@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ═════════════════════════════════════════
echo   Daily Rise - Установка
echo ═════════════════════════════════════════
echo.

:: Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python не найден!
    echo Установите Python с https://python.org
    pause
    exit /b 1
)
echo [OK] Python найден

:: Создание venv
if not exist "venv" (
    echo [INFO] Создание виртуального окружения...
    python -m venv venv
)
call venv\Scripts\activate.bat

:: Установка зависимостей
echo [INFO] Установка зависимостей...
pip install -q fastapi uvicorn sqlalchemy aiosqlite pydantic python-jose bcrypt python-multipart email-validator

:: Создание ярлыка
set DESKTOP=%USERPROFILE%\Desktop
echo [INFO] Создание ярлыка...

echo Set WshShell = WScript.CreateObject("WScript.Shell") > "%TEMP%\shortcut.vbs"
echo Set oLink = WshShell.CreateShortcut("%DESKTOP%\Daily Rise.lnk") >> "%TEMP%\shortcut.vbs"
echo oLink.TargetPath = "%CD%\run.vbs" >> "%TEMP%\shortcut.vbs"
echo oLink.WorkingDirectory = "%CD%" >> "%TEMP%\shortcut.vbs"
echo oLink.IconLocation = "%CD%\app\static\icon.svg" >> "%TEMP%\shortcut.vbs"
echo oLink.Description = "Daily Rise - Трекер привычек" >> "%TEMP%\shortcut.vbs"
echo oLink.Save >> "%TEMP%\shortcut.vbs"

cscript //nologo "%TEMP%\shortcut.vbs"
del "%TEMP%\shortcut.vbs"

:: Создание run.vbs
echo Set objShell = CreateObject("WScript.Shell") > run.vbs
echo objShell.Run "cmd /c venv\Scripts\activate.bat ^&^& start http://localhost:8000 ^&^& python -m uvicorn app.main:app --host 127.0.0.1 --port 8000", 0, False >> run.vbs

echo.
echo ═════════════════════════════════════════
echo   Готово!
echo ═════════════════════════════════════════
echo.
echo Ярлык Daily Rise создан на рабочем столе!
echo.
pause
