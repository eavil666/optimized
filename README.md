# Cloudflare CDN Fission Tool (Optimized)

这是优化后的Cloudflare CDN裂变工具，用于IP反查域名和域名解析IP，适用于CDN节点分析和网站资产发现场景。

## 代码结构

优化后的代码采用模块化设计，主要包含以下模块：

```
optimized/
├── __init__.py       # 包初始化文件
├── config.py         # 配置管理模块
├── network.py        # 网络请求模块
├── dns_utils.py      # DNS查询模块
├── main.py           # 主程序文件
├── requirements.txt  # 依赖包列表
└── README.md         # 使用说明
```

## 优化亮点

1. **模块化设计**：将功能拆分为配置、网络请求、DNS查询等独立模块
2. **面向对象**：使用类封装核心功能，提高代码可维护性
3. **配置管理**：使用数据类管理配置，支持从环境变量加载
4. **错误处理**：完善的异常捕获和错误信息输出
5. **性能优化**：使用dnspython库替代subprocess调用nslookup
6. **日志系统**：添加详细的日志记录，方便调试和监控
7. **命令行参数**：支持通过命令行参数自定义配置
8. **代码规范**：遵循PEP 8命名规范，添加详细的函数文档字符串

## 依赖安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```bash
python -m optimized.main
```

### 命令行参数

```
--ip-file          # IP列表文件路径 (默认: Fission_ip.txt)
--domain-file      # 域名列表文件路径 (默认: Fission_domain.txt)
--dns-result-file  # DNS查询结果文件路径 (默认: dns_result.txt)
--skip-ip-to-domain  # 跳过IP反查域名步骤
--skip-domain-to-ip  # 跳过域名解析IP步骤
```

### 示例

```bash
# 使用默认配置
python -m optimized.main

# 自定义IP和域名文件
python -m optimized.main --ip-file my_ips.txt --domain-file my_domains.txt

# 只执行域名解析IP步骤
python -m optimized.main --skip-ip-to-domain
```

## 配置说明

配置可以在`config.py`中修改，主要包括：

- 文件路径配置
- 并发数配置
- 网站配置
- 重试配置
- 请求超时

也可以通过环境变量设置配置，例如：

```bash
# 设置并发数
export MAX_WORKERS_REQUEST=30
export MAX_WORKERS_DNS=60

# 设置文件路径
export IPS_FILE=my_ips.txt
```

## 注意事项

1. 确保网络连接正常，工具需要访问互联网进行查询
2. 请合理设置并发数，避免对目标网站造成过大压力
3. 对于大量IP或域名的处理，可能需要较长时间，请耐心等待
4. 工具使用第三方库进行DNS查询，请确保依赖包已正确安装