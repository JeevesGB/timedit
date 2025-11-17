@echo off
REM TimEdit Launcher for Windows
REM This script starts the TimEdit application

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

REM Install requirements if needed
pip install -r requirements.txt >nul 2>&1

REM Start the application
python main.py

REM If there's an error, show it
if errorlevel 1 (
    echo.
    echo Error: Failed to start TimEdit
    echo Make sure all dependencies are installed: pip install -r requirements.txt
    pause
)
