# 🚀 БЫСТРАЯ СБОРКА APK - Copy & Paste для Google Colab

# ============================================================================
# ЯЧЕЙКА 1: Установка всех зависимостей (выполнить первой)
# ============================================================================
!pip install buildozer cython
!sudo apt-get update
!sudo apt-get install -y git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
!sudo update-alternatives --set java /usr/lib/jvm/java-11-openjdk-amd64/bin/java
print("✅ Зависимости установлены!")

# ============================================================================
# ЯЧЕЙКА 2: Подготовка проекта (выполнить второй)
# ============================================================================
import os
os.makedirs('/content/dailyrise', exist_ok=True)
os.chdir('/content/dailyrise')

# ВАЖНО: Замените ссылку на ваш репозиторий или загрузите файлы вручную
# Вариант A: Если репозиторий публичный
!git clone https://github.com/YOUR_USERNAME/habit_tracker.git

# Вариант B: Загрузка файлов вручную (раскомментировать если нужно)
# from google.colab import files
# uploaded = files.upload()  # Загрузите zip архив с проектом
# !unzip -q habit_tracker.zip -d /content/dailyrise

os.chdir('/content/dailyrise/habit_tracker/android-app')
print(f"📁 Текущая директория: {os.getcwd()}")
print("📄 Файлы:")
!ls -la

# ============================================================================
# ЯЧЕЙКА 3: Сборка APK (выполнить третьей, время: 15-25 минут)
# ============================================================================
print("🔨 Начинаем сборку APK...")
print("⏱ Это займёт 15-25 минут для первой сборки")
!buildozer -v android debug

# ============================================================================
# ЯЧЕЙКА 4: Скачивание готового APK (выполнить после сборки)
# ============================================================================
from google.colab import files
import glob

apk_files = glob.glob('bin/*.apk')
if apk_files:
    print(f"✅ APK найден: {apk_files[0]}")
    files.download(apk_files[0])
    print("📥 APK скачан на ваш компьютер!")
else:
    print("❌ APK не найден! Проверьте логи выше.")

# ============================================================================
# ЯЧЕЙКА 5 (опционально): Сохранение в Google Drive
# ============================================================================
# from google.colab import drive
# drive.mount('/content/drive')
# !cp bin/*.apk /content/drive/MyDrive/DailyRise/
# print("✅ APK сохранён в Google Drive!")
