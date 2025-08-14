# Cloudflare CDN Fission Tool (Optimized)

这是优化后的Cloudflare CDN裂变工具，用于IP反查域名和域名解析IP，适用于CDN节点分析和网站资产发现场景。

本项目灵感来源于 [CloudflareCDNFission](https://github.com/snowfal1/CloudflareCDNFission)，在此表示感谢。

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

###  Windows 系统安装说明

安装过程中，`lxml` 库可能需要编译环境。我们提供以下几种安装方式：

#### 方式 1: 使用专用 lxml 安装脚本 (推荐)

我们提供了一个专门用于安装 lxml 的 PowerShell 脚本，可以自动处理 Windows 环境下的安装问题：

```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install_lxml_windows.ps1
```

此脚本会：
1. 更新 pip
2. 安装 wheel
3. 尝试直接安装 lxml
4. 如果直接安装失败，会自动下载并安装预编译的 lxml wheel 文件

#### 方式 2: 使用通用安装脚本

我们还提供了一个通用的依赖安装脚本：

```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install_dependencies.ps1
```

脚本提供两种选项：
1. 标准安装 (需要 Visual C++ Build Tools)
2. 使用预编译 wheel 安装 (无需 Build Tools)

#### 方式 2: 手动安装

##### 选项 A: 安装 Visual C++ Build Tools 后使用 pip

1. 下载并安装 [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. 安装依赖：

```bash
pip install -r requirements.txt
```

##### 选项 B: 使用预编译 wheel

1. 首先安装 wheel 包：

```bash
pip install wheel
```

2. 安装 lxml 的预编译 wheel：

```bash
pip install --only-binary=lxml lxml>=4.9.3,<5.0.0
```

3. 安装剩余依赖：

```bash
pip install -r requirements.txt --no-deps
```

### macOS 和 Linux 系统

```bash
pip install -r requirements.txt

# 对于 Debian/Ubuntu 系统，如果 lxml 安装失败，可能需要安装:
# sudo apt-get install libxml2-dev libxslt1-dev

# 对于 CentOS/RHEL 系统:
# sudo yum install libxml2-devel libxslt-devel
```

## 使用方法

本工具提供了灵活的命令行接口，支持IP反查域名和域名解析IP功能。以下是详细使用说明：

### 基本使用

请确保在项目根目录下运行以下命令：

```bash
# 直接运行主脚本
python main.py
```

> 注意：根据项目实际结构，main.py位于项目根目录下，而非optimized目录中。之前的模块方式运行命令`python -m optimized.main`可能无法正常工作，因为项目结构不支持这种方式。

运行后，工具将依次执行IP反查域名和域名解析IP操作，并将结果保存到指定文件中。

> 注意：如果使用方法2，请确保先进入optimized目录，否则可能会出现文件路径错误。

### 命令行参数

工具支持以下命令行参数来自定义操作：

```
--ip-file <file_path>          # 指定IP列表文件路径（默认：Fission_ip.txt）
--domain-file <file_path>      # 指定域名列表文件路径（默认：Fission_domain.txt）
--dns-result-file <file_path>  # 指定DNS查询结果文件路径（默认：dns_result.txt）
--skip-ip-to-domain            # 跳过IP反查域名步骤，仅执行域名解析IP操作
--skip-domain-to-ip            # 跳过域名解析IP步骤，仅执行IP反查域名操作
--max-workers-request <num>    # 设置HTTP请求最大并发数（默认：30）
--max-workers-dns <num>        # 设置DNS查询最大并发数（默认：60）
--timeout <seconds>            # 设置请求超时时间（默认：10秒）
--retry-count <num>            # 设置请求失败重试次数（默认：3次）
```

### 使用示例

#### 1. 使用默认配置运行

```bash
python  main.py
```

此命令将使用默认的IP和域名列表文件，执行完整的IP反查域名和域名解析IP操作。

#### 2. 自定义IP和域名文件

```bash
python  main.py --ip-file my_ips.txt --domain-file my_domains.txt
```

使用自定义的IP列表文件`my_ips.txt`和域名列表文件`my_domains.txt`。

#### 3. 只执行域名解析IP步骤

```bash
python  main.py --skip-ip-to-domain
```

跳过IP反查域名步骤，仅执行域名解析IP操作。

#### 4. 只执行IP反查域名步骤

```bash
python  main.py --skip-domain-to-ip    
```

跳过域名解析IP步骤，仅执行IP反查域名操作。

#### 5. 自定义输出文件

```bash
python  main.py --dns-result-file my_results.txt
```

将结果保存到自定义文件`my_results.txt`中。

#### 6. 调整并发数和超时设置

```bash
python  main.py --max-workers-request 50 --max-workers-dns 100 --timeout 15
```

增加HTTP请求并发数到50，DNS查询并发数到100，设置请求超时时间为15秒。

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