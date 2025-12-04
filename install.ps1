# Audio.TUI Installer for Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "       Audio.TUI Installer              " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$ErrorActionPreference = "Stop"
$AppDir = Get-Location
$VenvDir = "$AppDir\venv"
$BinName = "aud"

# 1. Check for Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Detected $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/"
    Write-Host "Make sure to check 'Add Python to PATH' during installation."
    exit 1
}

# 2. Setup Virtual Environment
Write-Host "Setting up Python virtual environment..." -ForegroundColor Green
if (-not (Test-Path $VenvDir)) {
    python -m venv $VenvDir
    Write-Host "Created venv."
} else {
    Write-Host "venv already exists."
}

# 3. Install Dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Green
& "$VenvDir\Scripts\python.exe" -m pip install --upgrade pip
& "$VenvDir\Scripts\python.exe" -m pip install -r requirements.txt

# 4. Create 'aud' command (Batch wrapper)
Write-Host "Creating '$BinName' command..." -ForegroundColor Green
$WrapperPath = "$AppDir\$BinName.bat"
$Content = "@echo off
cd /d ""%~dp0""
call ""venv\Scripts\activate.bat""
python ""app.py"" %*
"
Set-Content -Path $WrapperPath -Value $Content

# 5. Add to PATH (User Environment Variable)
$CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($CurrentPath -notlike "*$AppDir*") {
    Write-Host "Adding installation directory to PATH..." -ForegroundColor Yellow
    [Environment]::SetEnvironmentVariable("Path", "$CurrentPath;$AppDir", "User")
    Write-Host "Added to PATH." -ForegroundColor Green
} else {
    Write-Host "Directory already in PATH."
}

# 6. Audio Driver Info
Write-Host "`nAudio Driver Setup:" -ForegroundColor Yellow
Write-Host "To capture system audio on Windows, you need VB-Audio Virtual Cable."
Write-Host "Download it here: https://vb-audio.com/Cable/"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Please restart your terminal (PowerShell/CMD)."
Write-Host "Then type '$BinName' to start the app."
