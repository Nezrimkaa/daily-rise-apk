#!/bin/bash
# Скрипт для сборки APK через WSL2
# Запускать после перезагрузки: wsl bash -c "cd /mnt/c/Users/Илья/habit_tracker/android-app && ./build_apk.sh"

set -e

echo "🚀 Начало сборки Daily Rise APK"
echo "================================"

# Переходим в директорию проекта
cd /mnt/c/Users/Илья/habit_tracker/android-app

# Обновляем пакеты
echo "📦 Обновление пакетов..."
sudo apt-get update -y

# Устанавливаем зависимости
echo "📦 Установка зависимостей..."
sudo apt-get install -y \
    python3 python3-pip python3-venv \
    git zip unzip openjdk-11-jdk autoconf libtool \
    pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev \
    wget curl

# Настройка Java
echo "☕ Настройка Java..."
sudo update-alternatives --set java /usr/lib/jvm/java-11-openjdk-amd64/bin/java
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Установка buildozer
echo "🔨 Установка buildozer..."
pip3 install --user buildozer cython

# Добавляем путь к бинарникам
export PATH=$PATH:~/.local/bin

# Инициализация (если нет buildozer.spec)
if [ ! -f "buildozer.spec" ]; then
    echo "📝 Инициализация buildozer..."
    buildozer init
fi

# Очистка предыдущей сборки
echo "🧹 Очистка предыдущей сборки..."
buildozer android clean || true

# Запуск сборки
echo "🔨 НАЧАЛО СБОРКИ APK (это займёт 15-25 минут)..."
echo "   Время начала: $(date)"
buildozer -v android debug

echo ""
echo "✅ СБОРКА ЗАВЕРШЕНА!"
echo "===================="
echo "📦 APK находится в: bin/*.apk"
echo "📂 Полный путь: /mnt/c/Users/Илья/habit_tracker/android-app/bin/"
echo ""
echo "Для установки на телефон:"
echo "1. Скопируйте APK из папки bin/"
echo "2. Включите 'Неизвестные источники' на телефоне"
echo "3. Установите APK"
