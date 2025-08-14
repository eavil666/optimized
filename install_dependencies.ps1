#!/usr/bin/env pwsh

# Script to install dependencies for the project on Windows

Write-Host "=== Fission Project Dependency Installer ==="
Write-Host ""

function Install-Dependencies {
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
    }
}

Install-Dependencies

Write-Host ""
Write-Host "After installation, activate the virtual environment with:"
Write-Host ".\venv\Scripts\Activate.ps1"
Write-Host "Then run the program with:"
Write-Host "python main.py"