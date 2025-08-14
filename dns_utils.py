# DNS查询模块
import os
import re
import ipaddress
import concurrent.futures
from typing import List, Set, Tuple, Dict

import dns.resolver

from config import config


def dns_lookup(domain: str) -> Tuple[str, str]:
    """执行DNS查询

    Args:
        domain: 域名

    Returns:
        Tuple[str, str]: (域名, 查询结果字符串)
    """
    print(f"Performing DNS lookup for {domain}...")
    try:
        # 使用dnspython进行DNS查询
        answers = dns.resolver.resolve(domain, 'A')
        result = f"Server: Unspecified\nAddress: 0.0.0.0#53\n\nNon-authoritative answer:\n{domain} canonical name = {domain}.\nName: {domain}\nAddress: {', '.join([str(rdata) for rdata in answers])}\n"
        return domain, result
    except Exception as e:
        error_msg = f"Server: Unspecified\nAddress: 0.0.0.0#53\n\n** server can't find {domain}: NXDOMAIN\nError: {str(e)}"
        return domain, error_msg


def perform_dns_lookups(domain_filename: str, result_filename: str, unique_ipv4_filename: str) -> None:
    """批量执行DNS查询并处理结果

    Args:
        domain_filename: 包含域名列表的文件名
        result_filename: 保存查询结果的文件名
        unique_ipv4_filename: 保存唯一IPv4地址的文件名
    """
    try:
        # 读取域名列表
        with open(domain_filename, 'r') as file:
            domains = file.read().splitlines()

        # 过滤空行
        domains = [domain.strip() for domain in domains if domain.strip()]

        if not domains:
            print("No domains found in file.")
            return

        # 并发执行DNS查询
        with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_workers_dns) as executor:
            results = list(executor.map(dns_lookup, domains))

        # 写入查询结果到文件
        with open(result_filename, 'w') as output_file:
            for domain, output in results:
                output_file.write(f"--- DNS Lookup for {domain} ---\n")
                output_file.write(output)
                output_file.write("\n\n")

        # 提取所有IPv4地址
        ipv4_addresses = set()
        for _, output in results:
            ipv4_addresses.update(re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', output))

        # 读取已存在的IP列表
        exist_list = set()
        if os.path.exists(unique_ipv4_filename):
            with open(unique_ipv4_filename, 'r') as file:
                exist_list = {ip.strip() for ip in file}

        # 过滤公网IP
        filtered_ipv4_addresses = set()
        for ip in ipv4_addresses:
            try:
                ip_obj = ipaddress.ip_address(ip)
                if ip_obj.is_global:
                    filtered_ipv4_addresses.add(ip)
            except ValueError:
                continue

        # 合并现有IP和新IP
        filtered_ipv4_addresses.update(exist_list)

        # 保存IPv4地址
        with open(unique_ipv4_filename, 'w') as output_file:
            for address in sorted(filtered_ipv4_addresses):
                output_file.write(address + '\n')

        print(f"DNS lookups completed. Found {len(filtered_ipv4_addresses)} unique IPv4 addresses.")

    except Exception as e:
        print(f"Error performing DNS lookups: {e}")
        raise