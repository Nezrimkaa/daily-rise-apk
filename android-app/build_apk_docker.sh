#!/bin/bash
# Скрипт для локальной сборки APK через Docker

echo "🔨 Daily Rise - Сборка APK через Docker"
echo "========================================"

# Создаём лицензии Android SDK
mkdir -p ~/.android/licenses
echo "8933bad161af4178b1185d1a37fbf41ea5269c55" > ~/.android/licenses/android-sdk-license
echo "d56f5187479451eabf01fb78af6dfcb131a6481e" >> ~/.android/licenses/android-sdk-license
echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" >> ~/.android/licenses/android-sdk-license

echo "✅ Лицензии приняты"
echo "📦 Запуск Docker..."

# Запускаем сборку в Docker
docker run --rm -v $(pwd):/home/user/app -w /home/user/app ghcr.io/kivy/buildozer:latest buildozer android debug

echo ""
echo "========================================"
if [ -f "bin/*.apk" ]; then
    echo "✅ APK готов!"
    ls -lh bin/*.apk
else
    echo "❌ Ошибка сборки"
fi
