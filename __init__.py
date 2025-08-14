# 包初始化文件
from .config import config
from .network import get_network_manager
from .dns_utils import perform_dns_lookups

__all__ = ['config', 'get_network_manager', 'perform_dns_lookups']