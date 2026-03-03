@echo off
chcp 65001 >nul
echo =====================================================
echo    Daily Rise APK Builder через WSL2
echo =====================================================
echo.
echo ВАЖНО: Если вы видите ошибку WSL, перезагрузите компьютер!
echo.
echo Команда для запуска сборки после перезагрузки:
echo   wsl bash -c "/mnt/c/Users/Илья/habit_tracker/android-app/build_apk.sh"
echo.
echo =====================================================
echo.

REM Пробуем запустить WSL
wsl bash -c "/mnt/c/Users/Илья/habit_tracker/android-app/build_apk.sh"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =====================================================
    echo ОШИБКА: WSL не запущен или требует перезагрузки
    echo =====================================================
    echo.
    echo Выполните следующие шаги:
    echo   1. Перезагрузите компьютер
    echo   2. После загрузки откройте этот файл снова
    echo   3. Или запустите вручную в PowerShell:
    echo.
    echo      wsl bash -c "/mnt/c/Users/Илья/habit_tracker/android-app/build_apk.sh"
    echo.
    echo =====================================================
    pause
)
