@echo off
setlocal enabledelayedexpansion

echo Building Daily Rise desktop app...
echo.

cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo Python OK

REM Create venv if needed
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q fastapi uvicorn sqlalchemy aiosqlite pydantic python-jose bcrypt python-multipart email-validator pywebview pyinstaller

REM Build EXE
echo Building EXE file...
pyinstaller --onefile --windowed --name "DailyRise" --icon="app\static\icon.svg" --add-data "app;app" desktop.py

echo.
echo Build complete!
echo Check dist\DailyRise.exe
echo.

REM Create shortcut using simple method
if exist "dist\DailyRise.exe" (
    echo Creating shortcut...
    
    REM Copy to desktop manually
    copy "dist\DailyRise.exe" "%USERPROFILE%\Desktop\DailyRise.exe" >nul 2>&1
    
    if exist "%USERPROFILE%\Desktop\DailyRise.exe" (
        echo Shortcut created on desktop!
    ) else (
        echo Copy dist\DailyRise.exe to desktop manually
    )
)

echo.
pause
