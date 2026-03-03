@echo off
setlocal enabledelayedexpansion

echo ═════════════════════════════════════════
echo   Daily Rise - Быстрый запуск
echo ═════════════════════════════════════════
echo.

cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Install from https://python.org
    pause
    exit /b 1
)
echo [1/3] Python OK

REM Create venv if needed
if not exist "venv" (
    echo [2/3] Creating virtual environment...
    python -m venv venv
) else (
    echo [2/3] Virtual environment OK
)

call venv\Scripts\activate.bat

REM Install dependencies quietly
echo [3/3] Installing dependencies...
pip install -q fastapi uvicorn sqlalchemy aiosqlite pydantic python-jose bcrypt python-multipart email-validator

echo.
echo ═════════════════════════════════════════
echo   Запуск приложения...
echo ═════════════════════════════════════════
echo.

REM Run the app - will open in browser
python desktop.py

pause
