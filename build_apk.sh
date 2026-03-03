#!/bin/bash

# Daily Rise - Android APK Builder
# Использует Pydroid 3 для сборки APK

echo "═════════════════════════════════════════"
echo "  Daily Rise - Android APK Builder"
echo "═════════════════════════════════════════"
echo ""

# Проверка Python
if ! command -v python &> /dev/null; then
    echo "[ERROR] Python не найден!"
    exit 1
fi

echo "[INFO] Установка зависимостей..."
pip install buildozer cython

echo "[INFO] Инициализация Buildozer..."
buildozer init

# Копируем manifest в assets
cp app/static/manifest.json .
cp app/static/icon.svg .

echo "[INFO] Сборка APK..."
buildozer -v android debug

echo ""
echo "═════════════════════════════════════════"
echo "  Готово! APK в папке bin/"
echo "═════════════════════════════════════════"
