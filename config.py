# 配置管理模块
import os
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class SiteConfig:
    url: str
    xpath: str


@dataclass
class Config:
    # 文件路径配置
    ips_file: str = "Fission_ip.txt"
    domains_file: str = "Fission_domain.txt"
    dns_result_file: str = "dns_result.txt"

    # 并发数配置
    max_workers_request: int = 20
    max_workers_dns: int = 50

    # 网站配置
    sites_config: Dict[str, SiteConfig] = None

    # 重试配置
    max_retries: int = 5
    backoff_factor: float = 0.3
    retry_status_codes: List[int] = None

    # 请求超时
    request_timeout: int = 10

    def __post_init__(self):
        # 初始化网站配置
        if self.sites_config is None:
            self.sites_config = {
                "site_ip138": SiteConfig(
                    url="https://site.ip138.com/",
                    xpath='//ul[@id="list"]/li/a'
                ),
                "dnsdblookup": SiteConfig(
                    url="https://dnsdblookup.com/",
                    xpath='//ul[@id="list"]/li/a'
                ),
                "ipchaxun": SiteConfig(
                    url="https://ipchaxun.com/",
                    xpath='//div[@id="J_domain"]/p/a'
                )
            }

        # 初始化重试状态码
        if self.retry_status_codes is None:
            self.retry_status_codes = [500, 502, 503, 504]

    @classmethod
    def from_env(cls):
        """从环境变量加载配置"""
        config = cls()

        # 从环境变量读取配置，如果不存在则使用默认值
        config.ips_file = os.getenv("IPS_FILE", config.ips_file)
        config.domains_file = os.getenv("DOMAINS_FILE", config.domains_file)
        config.dns_result_file = os.getenv("DNS_RESULT_FILE", config.dns_result_file)

        # 并发数配置
        if os.getenv("MAX_WORKERS_REQUEST"):
            config.max_workers_request = int(os.getenv("MAX_WORKERS_REQUEST"))
        if os.getenv("MAX_WORKERS_DNS"):
            config.max_workers_dns = int(os.getenv("MAX_WORKERS_DNS"))

        return config


# 创建配置实例
config = Config()