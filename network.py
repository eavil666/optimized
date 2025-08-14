# 网络请求模块
import random
import concurrent.futures
from typing import List, Set, Dict

import requests
from html.parser import HTMLParser
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import config


class NetworkManager:
    """网络请求管理器，负责处理所有网络请求相关操作"""

    def __init__(self):
        """初始化网络管理器"""
        self.ua = UserAgent()
        self.session = self._setup_session()

    def _setup_session(self) -> requests.Session:
        """设置请求会话，配置重试策略

        Returns:
            requests.Session: 配置好的会话对象
        """
        session = requests.Session()
        retries = Retry(
            total=config.max_retries,
            backoff_factor=config.backoff_factor,
            status_forcelist=config.retry_status_codes
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _get_headers(self) -> Dict[str, str]:
        """生成随机请求头

        Returns:
            Dict[str, str]: 请求头字典
        """
        return {
            'User-Agent': self.ua.random,
            'Accept': '*/*',
            'Connection': 'keep-alive',
        }

    def fetch_domains_for_ip(self, ip_address: str, attempts: int = 0, used_sites: List[str] = None) -> List[str]:
        """根据IP地址查询域名

        Args:
            ip_address: IP地址
            attempts: 已尝试次数
            used_sites: 已使用的网站

        Returns:
            List[str]: 域名列表
        """
        print(f"Fetching domains for {ip_address}...")
        if used_sites is None:
            used_sites = []
        if attempts >= 3:
            print(f"Max attempts reached for {ip_address}")
            return []

        # 选择一个未使用的网站
        available_sites = {k: v for k, v in config.sites_config.items() if k not in used_sites}
        if not available_sites:
            print(f"No available sites for {ip_address}")
            return []

        site_key = random.choice(list(available_sites.keys()))
        site_info = available_sites[site_key]
        used_sites.append(site_key)

        try:
            url = f"{site_info.url}{ip_address}/"
            headers = self._get_headers()
            response = self.session.get(url, headers=headers, timeout=config.request_timeout)
            response.raise_for_status()
            html_content = response.text

            # 使用HTMLParser解析HTML
            class DomainParser(HTMLParser):
                def __init__(self, xpath):
                    super().__init__()
                    self.domains = []
                    self.current_ul_id = None
                    self.current_div_id = None
                    self.current_p_tag = False
                    self.current_a_tag = False
                    
                    # 确定要提取的模式
                    if 'ul[@id="list"]/li/a' in xpath:
                        self.mode = 'ul_list'
                    elif 'div[@id="J_domain"]/p/a' in xpath:
                        self.mode = 'div_domain'
                    else:
                        self.mode = 'unknown'
                        print(f"Warning: Unsupported XPath: {xpath}")

                def handle_starttag(self, tag, attrs):
                    if tag == 'ul':
                        for attr, value in attrs:
                            if attr == 'id' and value == 'list':
                                self.current_ul_id = 'list'
                                break
                    elif tag == 'div':
                        for attr, value in attrs:
                            if attr == 'id' and value == 'J_domain':
                                self.current_div_id = 'J_domain'
                                break
                    elif tag == 'p' and self.current_div_id == 'J_domain':
                        self.current_p_tag = True
                    elif tag == 'a':
                        if (self.current_ul_id == 'list' and tag == 'a') or \
                           (self.current_div_id == 'J_domain' and self.current_p_tag and tag == 'a'):
                            self.current_a_tag = True
                        
                def handle_endtag(self, tag):
                    if tag == 'ul' and self.current_ul_id == 'list':
                        self.current_ul_id = None
                    elif tag == 'div' and self.current_div_id == 'J_domain':
                        self.current_div_id = None
                    elif tag == 'p' and self.current_p_tag:
                        self.current_p_tag = False
                    elif tag == 'a' and self.current_a_tag:
                        self.current_a_tag = False

                def handle_data(self, data):
                    if self.current_a_tag and data.strip():
                        self.domains.append(data.strip())

            parser = DomainParser(site_info.xpath)
            parser.feed(html_content)
            domains = parser.domains

            if domains:
                print(f"Successfully fetched domains for {ip_address} from {site_info.url}")
                return domains
            else:
                raise Exception("No domains found")

        except Exception as e:
            print(f"Error fetching domains for {ip_address} from {site_info.url}: {e}")
            return self.fetch_domains_for_ip(ip_address, attempts + 1, used_sites)

    def fetch_domains_concurrently(self, ip_addresses: List[str]) -> List[str]:
        """并发查询多个IP地址对应的域名

        Args:
            ip_addresses: IP地址列表

        Returns:
            List[str]: 去重后的域名列表
        """
        domains = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_workers_request) as executor:
            future_to_ip = {executor.submit(self.fetch_domains_for_ip, ip): ip for ip in ip_addresses}
            for future in concurrent.futures.as_completed(future_to_ip):
                domains.extend(future.result())

        return list(set(domains))


def get_network_manager() -> NetworkManager:
    """获取网络管理器实例

    Returns:
        NetworkManager: 网络管理器实例
    """
    return NetworkManager()