#!/usr/bin/env pwsh

# 安装lxml的Windows专用脚本
# 此脚本使用wheel来安装预编译版本的lxml，避免编译错误

# 更新pip
Write-Host "更新pip..."
python -m pip install --upgrade pip

# 安装wheel
Write-Host "安装wheel..."
python -m pip install wheel>=0.41.2

# 尝试安装lxml
Write-Host "尝试安装lxml..."
$lxmlInstallResult = python -m pip install lxml>=4.9.3,<5.0.0 2>&1

# 检查安装是否成功
if ($LASTEXITCODE -eq 0) {
    Write-Host "lxml安装成功!"
} else {
    Write-Host "lxml直接安装失败，尝试使用预编译wheel..."

    # 安装预编译wheel (这里使用lxml 4.9.3作为示例)
    # 注意：实际使用时可能需要根据Python版本和系统架构选择正确的wheel文件
    $pythonVersion = python -c "import sys; print(f'{sys.version_info.major}{sys.version_info.minor}')"
    $wheelUrl = "https://download.lfd.uci.edu/pythonlibs/w6aqbg5k/lxml-4.9.3-cp${pythonVersion}-cp${pythonVersion}-win_amd64.whl"
    $wheelFile = "lxml-4.9.3-cp${pythonVersion}-cp${pythonVersion}-win_amd64.whl"

    # 下载wheel文件
    Write-Host "下载预编译wheel文件: $wheelUrl"
    Invoke-WebRequest -Uri $wheelUrl -OutFile $wheelFile

    # 安装wheel文件
    Write-Host "安装预编译wheel文件..."
    python -m pip install $wheelFile

    # 清理wheel文件
    Remove-Item -Path $wheelFile -Force

    # 再次检查安装是否成功
    if ($LASTEXITCODE -eq 0) {
        Write-Host "lxml通过预编译wheel安装成功!"
    } else {
        Write-Host "lxml安装失败，请尝试手动安装或检查系统环境。"
        Write-Host "错误信息: $lxmlInstallResult"
    }
}