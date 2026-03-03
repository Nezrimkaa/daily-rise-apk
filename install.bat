@echo off
chcp 65001 >nul
title Daily Rise - Установка

echo ═════════════════════════════════════════
echo   Daily Rise - Установка приложения
echo ═════════════════════════════════════════
echo.

:: Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python не найден!
    echo Установите Python 3.10+ с https://python.org
    pause
    exit /b 1
)
echo [OK] Python найден

:: Проверка виртуального окружения
if not exist "venv" (
    echo [INFO] Создание виртуального окружения...
    python -m venv venv
)
echo [OK] Виртуальное окружение готово

:: Установка зависимостей
echo [INFO] Установка зависимостей...
call venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1
echo [OK] Зависимости установлены

echo.
echo ═════════════════════════════════════════
echo   Готово!
echo ═════════════════════════════════════════
echo.
echo Для запуска:
echo   1. Запустите start_app.bat
echo   2. Или откройте http://localhost:8000 в браузере
echo.
pause
