@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ═════════════════════════════════════════
echo   Daily Rise - Создание приложения
echo ═════════════════════════════════════════
echo.

cd /d "%~dp0"

:: Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python не найден!
    echo Установите Python 3.10+ с https://python.org
    pause
    exit /b 1
)
echo [OK] Python найден

:: Создание venv если нет
if not exist "venv" (
    echo [INFO] Создание виртуального окружения...
    python -m venv venv
)
echo [OK] Виртуальное окружение готово

:: Активация
call venv\Scripts\activate.bat

:: Установка зависимостей
echo [INFO] Установка зависимостей...
pip install -q -r requirements.txt

echo.
echo [INFO] Сборка приложения...
pip install -q pyinstaller

:: Сборка EXE
pyinstaller --onefile --windowed --name "Daily Rise" --icon="app\static\icon.svg" launcher_simple.py

echo.
echo ═════════════════════════════════════════
echo   Готово!
echo ═════════════════════════════════════════
echo.

:: Копирование необходимых файлов
if not exist "dist\app" mkdir "dist\app"
xcopy /E /I /Y "app" "dist\app" >nul
xcopy /Y "requirements.txt" "dist\" >nul

:: Создание ярлыка на рабочем столе
set DESKTOP=%USERPROFILE%\Desktop
if exist "dist\Daily Rise.exe" (
    echo [INFO] Создание ярлыка на рабочем столе...
    
    echo Set WshShell = WScript.CreateObject^("WScript.Shell"^) > "%TEMP%\create_shortcut.vbs"
    echo Set oLink = WshShell.CreateShortcut^("%DESKTOP%\Daily Rise.lnk"^) >> "%TEMP%\create_shortcut.vbs"
    echo oLink.TargetPath = "%CD%\dist\Daily Rise.exe" >> "%TEMP%\create_shortcut.vbs"
    echo oLink.WorkingDirectory = "%CD%\dist" >> "%TEMP%\create_shortcut.vbs"
    echo oLink.Description = "Daily Rise - Трекер привычек" >> "%TEMP%\create_shortcut.vbs"
    echo oLink.Save >> "%TEMP%\create_shortcut.vbs"
    
    cscript //nologo "%TEMP%\create_shortcut.vbs"
    del "%TEMP%\create_shortcut.vbs"
    
    echo [OK] Ярлык создан на рабочем столе!
    echo.
    echo Приложение готово к запуску!
)

echo.
pause
