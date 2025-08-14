# 主程序模块
import os
import argparse
import logging
from typing import List, Set

from config import config
from network import get_network_manager
from dns_utils import perform_dns_lookups

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fission.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Fission:
    """Cloudflare CDN Fission工具主类"""

    def __init__(self):
        """初始化Fission工具"""
        self.network_manager = get_network_manager()

    def load_ip_list(self, file_path: str) -> List[str]:
        """从文件加载IP列表

        Args:
            file_path: IP列表文件路径

        Returns:
            List[str]: IP地址列表
        """
        if not os.path.exists(file_path):
            logger.warning(f"IP file not found: {file_path}. Creating empty file.")
            with open(file_path, 'w') as file:
                file.write('')
            return []

        with open(file_path, 'r') as file:
            return [ip.strip() for ip in file if ip.strip()]

    def load_domain_list(self, file_path: str) -> List[str]:
        """从文件加载域名列表

        Args:
            file_path: 域名列表文件路径

        Returns:
            List[str]: 域名列表
        """
        if not os.path.exists(file_path):
            logger.warning(f"Domain file not found: {file_path}. Creating empty file.")
            with open(file_path, 'w') as file:
                file.write('')
            return []

        with open(file_path, 'r') as file:
            return [domain.strip() for domain in file if domain.strip()]

    def save_domain_list(self, domains: List[str], file_path: str) -> None:
        """保存域名列表到文件

        Args:
            domains: 域名列表
            file_path: 保存文件路径
        """
        with open(file_path, 'w') as output:
            for domain in domains:
                output.write(domain + '\n')
        logger.info(f"Saved {len(domains)} domains to {file_path}")

    def ip_to_domain(self) -> None:
        """IP反查域名"""
        logger.info("Starting IP to domain lookup...")

        # 加载IP列表
        ip_list = self.load_ip_list(config.ips_file)
        if not ip_list:
            logger.warning("No IP addresses found. Skipping IP to domain lookup.")
            return

        logger.info(f"Found {len(ip_list)} IP addresses to process.")

        # 并发查询域名
        domain_list = self.network_manager.fetch_domains_concurrently(ip_list)
        logger.info(f"Found {len(domain_list)} new domains from IP lookup.")

        # 加载已存在的域名列表
        exist_domains = self.load_domain_list(config.domains_file)
        logger.info(f"Found {len(exist_domains)} existing domains.")

        # 合并并去重
        combined_domains = list(set(domain_list + exist_domains))
        logger.info(f"Total unique domains after merging: {len(combined_domains)}")

        # 保存结果
        self.save_domain_list(combined_domains, config.domains_file)
        logger.info("IP to domain lookup completed.")

    def domain_to_ip(self) -> None:
        """域名解析IP"""
        logger.info("Starting domain to IP lookup...")

        # 执行DNS查询
        perform_dns_lookups(
            domain_filename=config.domains_file,
            result_filename=config.dns_result_file,
            unique_ipv4_filename=config.ips_file
        )

        logger.info("Domain to IP lookup completed.")

    def run(self) -> None:
        """运行完整流程"""
        logger.info("Starting Fission process...")

        # IP反查域名
        self.ip_to_domain()

        # 域名解析IP
        self.domain_to_ip()

        logger.info("Fission process completed successfully.")


def main():
    """程序入口"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Cloudflare CDN Fission Tool')
    parser.add_argument('--ip-file', help='Path to IP list file', default=config.ips_file)
    parser.add_argument('--domain-file', help='Path to domain list file', default=config.domains_file)
    parser.add_argument('--dns-result-file', help='Path to DNS result file', default=config.dns_result_file)
    parser.add_argument('--skip-ip-to-domain', action='store_true', help='Skip IP to domain lookup')
    parser.add_argument('--skip-domain-to-ip', action='store_true', help='Skip domain to IP lookup')
    args = parser.parse_args()

    # 更新配置
    config.ips_file = args.ip_file
    config.domains_file = args.domain_file
    config.dns_result_file = args.dns_result_file

    # 创建Fission实例
    fission = Fission()

    # 运行流程
    if not args.skip_ip_to_domain:
        fission.ip_to_domain()
    else:
        logger.info("Skipping IP to domain lookup as requested.")

    if not args.skip_domain_to_ip:
        fission.domain_to_ip()
    else:
        logger.info("Skipping domain to IP lookup as requested.")

    logger.info("Program execution completed.")

if __name__ == '__main__':
    main()
