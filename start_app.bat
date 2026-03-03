@echo off
chcp 65001 >nul
title Daily Rise

cd /d "%~dp0"

echo ═════════════════════════════════════════
echo   🌱 Daily Rise - Трекер привычек
echo ═════════════════════════════════════════
echo.

:: Проверка venv
if not exist "venv" (
    echo [ERROR] Виртуальное окружение не найдено!
    echo Запустите install.bat для установки.
    pause
    exit /b 1
)

:: Запуск лаунчера
call venv\Scripts\activate.bat
python launcher.py

pause
