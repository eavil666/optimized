#!/usr/bin/env pwsh

# Script to install dependencies for the project on Windows
# This script provides two options for installing lxml:
# 1. Standard pip install (requires Visual C++ Build Tools)
# 2. Installation via precompiled wheel (for users without Build Tools)

Write-Host "=== Fission Project Dependency Installer ==="
Write-Host ""

# Option 1: Standard installation with pip
function Install-Standard {
    Write-Host "[Option 1] Standard installation with pip"
    Write-Host "Note: This requires Visual C++ Build Tools to be installed."
    Write-Host "If you don't have them, you can download from:"
    Write-Host "https://visualstudio.microsoft.com/visual-cpp-build-tools/"
    Write-Host ""

    try {
        Write-Host "Creating virtual environment..."
        python -m venv venv
        Write-Host "Activating virtual environment..."
        . .\venv\Scripts\Activate.ps1
        Write-Host "Upgrading pip..."
        python -m pip install --upgrade pip
        Write-Host "Installing dependencies from requirements.txt..."
        pip install -r requirements.txt
        Write-Host ""
        Write-Host "✅ Dependencies installed successfully!"
    } catch {
        Write-Host "❌ Error during installation: $_"
        Write-Host ""
        Write-Host "Try using Option 2 with precompiled wheels."
    }
}

# Option 2: Installation with precompiled wheels
function Install-With-Wheels {
    Write-Host "[Option 2] Installation with precompiled wheels"
    Write-Host "This option uses precompiled lxml wheels from PyPI."
    Write-Host ""

    try {
        Write-Host "Creating virtual environment..."
        python -m venv venv
        Write-Host "Activating virtual environment..."
        . .\venv\Scripts\Activate.ps1
        Write-Host "Upgrading pip..."
        python -m pip install --upgrade pip
        Write-Host "Installing wheel..."
        pip install wheel
        Write-Host "Installing lxml with precompiled wheel..."
        # Install lxml separately first with --only-binary option
        pip install --only-binary=lxml lxml>=4.9.3,<5.0.0
        Write-Host "Installing remaining dependencies..."
        pip install -r requirements.txt --no-deps
        Write-Host ""
        Write-Host "✅ Dependencies installed successfully!"
    } catch {
        Write-Host "❌ Error during installation: $_"
    }
}

# Display menu
Write-Host "Please choose an installation option:"
Write-Host "1. Standard installation (requires Visual C++ Build Tools)"
Write-Host "2. Installation with precompiled wheels (no Build Tools needed)"

$choice = Read-Host "Enter your choice (1 or 2)"

switch ($choice) {
    '1' {
        Install-Standard
    }
    '2' {
        Install-With-Wheels
    }
    default {
        Write-Host "❌ Invalid choice. Please run the script again and select 1 or 2."
    }
}

Write-Host ""
Write-Host "After installation, activate the virtual environment with:"
Write-Host ".\venv\Scripts\Activate.ps1"
Write-Host "Then run the program with:"
Write-Host "python main.py"