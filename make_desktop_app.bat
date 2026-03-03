@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ════════════════════════════════════════════════════════════
echo   Daily Rise - Создание desktop приложения
echo ════════════════════════════════════════════════════════════
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

:: Создание venv
if not exist "venv" (
    echo [INFO] Создание виртуального окружения...
    python -m venv venv
)
echo [OK] Виртуальное окружение готово

call venv\Scripts\activate.bat

:: Установка зависимостей
echo.
echo [INFO] Установка зависимостей...
pip install -q fastapi uvicorn sqlalchemy aiosqlite pydantic python-jose bcrypt python-multipart email-validator pywebview pyinstaller

:: Сборка EXE
echo.
echo [INFO] Сборка EXE файла...
pyinstaller --onefile --windowed --name "Daily Rise" --icon="app\static\icon.svg" --add-data "app;app" desktop.py

echo.
echo ════════════════════════════════════════════════════════════
echo   Готово!
echo ════════════════════════════════════════════════════════════
echo.

:: Копирование venv в dist
if exist "dist\Daily Rise.exe" (
    echo [INFO] Копирование необходимых файлов...
    
    if not exist "dist\venv" mkdir "dist\venv"
    xcopy /E /I /Y "venv\Lib\site-packages" "dist\venv\Lib\site-packages" >nul
    xcopy /E /I /Y "venv\Scripts" "dist\venv\Scripts" >nul
    xcopy /Y "venv\pyvenv.cfg" "dist\venv\" >nul
    
    :: Копирование app
    if not exist "dist\app" mkdir "dist\app"
    xcopy /E /I /Y "app" "dist\app" >nul
    
    echo [OK] Файлы скопированы!
    echo.
    echo Приложение: dist\Daily Rise.exe
    echo.
    
    :: Создание ярлыка
    set DESKTOP=%USERPROFILE%\Desktop
    
    echo [INFO] Создание ярлыка на рабочем столе...
    
    :: Используем PowerShell для создания ярлыка
    powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Daily Rise.lnk'); $Shortcut.TargetPath = '%CD%\dist\Daily Rise.exe'; $Shortcut.WorkingDirectory = '%CD%\dist'; $Shortcut.Description = 'Daily Rise - Трекер привычек'; $Shortcut.Save()"
    
    if exist "%DESKTOP%\Daily Rise.lnk" (
        echo [OK] Ярлык создан!
    ) else (
        echo [!] Не удалось создать ярлык автоматически.
        echo     Создайте вручную из dist\Daily Rise.exe
    )
    
    echo.
    echo ════════════════════════════════════════════════════════════
    echo   Приложение готово к запуску!
    echo ════════════════════════════════════════════════════════════
    echo.
    echo Запустите: dist\Daily Rise.exe
    echo Или используйте ярлык на рабочем столе
    echo.
)

pause
