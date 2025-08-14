# 使用BeautifulSoup解析HTML的模块
from typing import List
from bs4 import BeautifulSoup


class SoupDomainParser:
    """使用BeautifulSoup解析HTML以提取域名的解析器

    这个类提供了一种更简洁、更灵活的方式来解析HTML内容
    并提取其中的域名信息，替代传统的HTMLParser实现。
    """

    def __init__(self):
        """初始化解析器"""
        pass

    def parse_domains(self, html_content: str, xpath: str) -> List[str]:
        """解析HTML内容并提取域名

        Args:
            html_content: HTML内容字符串
            xpath: 用于定位域名的XPath-like表达式

        Returns:
            List[str]: 提取的域名列表
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        domains = []

        # 根据不同的XPath模式提取域名
        if 'ul[@id="list"]/li/a' in xpath:
            # 处理ul列表模式
            ul_element = soup.find('ul', id='list')
            if ul_element:
                for a_tag in ul_element.find_all('a'):
                    domain = a_tag.get_text(strip=True)
                    if domain:
                        domains.append(domain)

        elif 'div[@id="J_domain"]/p/a' in xpath:
            # 处理div域名模式
            div_element = soup.find('div', id='J_domain')
            if div_element:
                for p_tag in div_element.find_all('p'):
                    a_tag = p_tag.find('a')
                    if a_tag:
                        domain = a_tag.get_text(strip=True)
                        if domain:
                            domains.append(domain)

        else:
            print(f"Warning: Unsupported XPath pattern: {xpath}")

        return domains


def get_soup_parser() -> SoupDomainParser:
    """获取SoupDomainParser实例

    Returns:
        SoupDomainParser: 解析器实例
    """
    return SoupDomainParser()