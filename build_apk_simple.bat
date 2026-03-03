@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo   Daily Rise - Создание Android APK
echo ============================================================
echo.

echo [INFO] APK будет создан через онлайн сервис
echo.
echo СПОСОБ 1 (Быстрый - через веб):
echo.
echo 1. Открой https://pwabuilder.com
echo 2. Введи URL своего приложения
echo 3. Нажми "Build for Android"
echo 4. Скачай APK
echo.
echo ----------------------------------------------------------
echo.
echo СПОСОБ 2 (Локально - нужен Python + Kivy):
echo.
echo 1. Установи Kivy:
echo    pip install kivy
echo.
echo 2. Установи buildozer (Linux/Mac):
echo    pip install buildozer
echo.
echo 3. Запусти сборку:
echo    buildozer android debug
echo.
echo APK будет в: bin/*.apk
echo.
echo ============================================================
echo.

REM Проверяем Kivy
python -c "import kivy" >nul 2>&1
if not errorlevel 1 (
    echo [OK] Kivy найден
    echo.
    echo Хотите собрать APK сейчас? (Y/N)
    set /p choice=
    if /i "!choice!"=="Y" (
        echo.
        echo [INFO] Запуск сборки...
        echo.
        cd /d "%~dp0android-app"
        buildozer android debug
        echo.
        echo APK в папке: bin\
    )
) else (
    echo [!] Kivy не найден
    echo.
    echo Для локальной сборки установи:
    echo   pip install kivy buildozer
    echo.
    echo Или используй онлайн сервис:
    echo   https://pwabuilder.com
)

echo.
pause
