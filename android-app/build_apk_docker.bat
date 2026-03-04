@echo off
REM Скрипт для локальной сборки APK через Docker (Windows)

echo ========================================
echo Daily Rise - Сборка APK через Docker
echo ========================================

REM Создаём лицензии Android SDK
if not exist "%USERPROFILE%\.android\licenses" mkdir "%USERPROFILE%\.android\licenses"
echo 8933bad161af4178b1185d1a37fbf41ea5269c55 > "%USERPROFILE%\.android\licenses\android-sdk-license"
echo d56f5187479451eabf01fb78af6dfcb131a6481e >> "%USERPROFILE%\.android\licenses\android-sdk-license"
echo 24333f8a63b6825ea9c5514f83c2829b004d1fee >> "%USERPROFILE%\.android\licenses\android-sdk-license"

echo ✅ Лицензии приняты
echo 📦 Запуск Docker...

REM Запускаем сборку в Docker
docker run --rm -v %CD%:/home/user/app -w /home/user/app ghcr.io/kivy/buildozer:latest buildozer android debug

echo.
echo ========================================
if exist "bin\*.apk" (
    echo ✅ APK готов!
    dir bin\*.apk
) else (
    echo ❌ Ошибка сборки
)
