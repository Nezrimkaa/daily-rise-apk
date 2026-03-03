@echo off
chcp 65001 >nul
echo ═════════════════════════════════════════
echo   Daily Rise - Создание приложения
echo ═════════════════════════════════════════
echo.

cd /d "%~dp0"

:: Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python не найден!
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
pip install -q pyinstaller pywebview

:: Сборка EXE
echo [INFO] Сборка приложения...
pyinstaller --onefile --windowed --name "Daily Rise" --icon="app\static\icon.svg" --add-data "app;app" app.py

echo.
echo ═════════════════════════════════════════
echo   Готово!
echo ═════════════════════════════════════════
echo.
echo Приложение в папке: dist\Daily Rise.exe
echo.

:: Создание ярлыка на рабочем столе
set DESKTOP=%USERPROFILE%\Desktop
if exist "dist\Daily Rise.exe" (
    echo [INFO] Создание ярлыка на рабочем столе...
    
    :: Создаём VBScript для ярлыка
    echo Set WshShell = WScript.CreateObject("WScript.Shell") > "%TEMP%\create_shortcut.vbs"
    echo Set oLink = WshShell.CreateShortcut("%DESKTOP%\Daily Rise.lnk") >> "%TEMP%\create_shortcut.vbs"
    echo oLink.TargetPath = "%CD%\dist\Daily Rise.exe" >> "%TEMP%\create_shortcut.vbs"
    echo oLink.WorkingDirectory = "%CD%" >> "%TEMP%\create_shortcut.vbs"
    echo oLink.Description = "Daily Rise - Трекер привычек" >> "%TEMP%\create_shortcut.vbs"
    echo oLink.Save >> "%TEMP%\create_shortcut.vbs"
    
    cscript //nologo "%TEMP%\create_shortcut.vbs"
    del "%TEMP%\create_shortcut.vbs"
    
    echo [OK] Ярлык создан!
)

echo.
echo Нажмите любую клавишу для выхода...
pause >nul
