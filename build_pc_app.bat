@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo   Daily Rise - Создание PC приложения (EXE)
echo ============================================================
echo.

cd /d "%~dp0pc-app"

REM Проверка Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js не найден!
    echo Установите Node.js с https://nodejs.org
    echo.
    pause
    exit /b 1
)
echo [OK] Node.js найден

REM Копирование backend
echo [1/4] Копирование файлов...
if exist "backend" rmdir /s /q "backend"
mkdir "backend"
xcopy /E /I /Y "..\app" "backend\app" >nul
xcopy /E /I /Y "..\venv" "backend\venv" >nul
copy "..\requirements.txt" "backend\" >nul
echo [OK] Файлы скопированы

REM Установка зависимостей
echo [2/4] Установка Node.js зависимостей...
call npm install
if errorlevel 1 (
    echo [ERROR] Ошибка установки npm пакетов
    pause
    exit /b 1
)
echo [OK] Зависимости установлены

REM Сборка
echo [3/4] Сборка EXE файла...
call npm run build
if errorlevel 1 (
    echo [ERROR] Ошибка сборки
    pause
    exit /b 1
)
echo [OK] Сборка завершена

REM Копирование на рабочий стол
echo [4/4] Копирование на рабочий стол...
set DESKTOP=%USERPROFILE%\Desktop
if exist "dist\Daily Rise.exe" (
    copy "dist\Daily Rise.exe" "%DESKTOP%\Daily Rise.exe" >nul 2>&1
    if exist "%DESKTOP%\Daily Rise.exe" (
        echo [OK] Ярлык создан на рабочем столе!
    )
)

echo.
echo ============================================================
echo   ГОТОВО!
echo ============================================================
echo.
echo Приложение: dist\Daily Rise.exe
echo Ярлык: Рабочий стол\Daily Rise.exe
echo.
echo Запустите Daily Rise.exe для использования!
echo.

pause
