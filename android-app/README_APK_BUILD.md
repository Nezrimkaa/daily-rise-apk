# Сборка APK для Daily Rise

## Офлайн-режим
Приложение работает **полностью офлайн** — бэкенд запускается прямо на телефоне, база данных хранится локально.

## Требования для сборки
- Linux/macOS (на Windows используйте WSL2, Docker или Google Colab)
- Python 3.8+
- Buildozer
- Java JDK 11
- Android SDK & NDK

## Быстрая сборка через Google Colab (рекомендуется)

1. Откройте [Google Colab](https://colab.research.google.com/)
2. Создайте новый блокнот и выполните:

```python
!pip install buildozer
!sudo apt-get install -y git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
!pip install --upgrade buildozer
!buildozer init
```

3. Скопируйте `buildozer.spec` из папки `android-app` в рабочую директорию Colab
4. Скопируйте папку `app` в рабочую директорию Colab
5. Выполните сборку:

```python
!buildozer -v android debug
```

6. Скачайте готовый APK из `/content/bin/`

## Сборка на Linux

```bash
cd android-app
buildozer init  # если нет buildozer.spec
buildozer -v android debug
```

Готовый APK: `bin/dailyrise-0.1-1-debug.apk`

## Установка на телефон

1. Включите "Установку из неизвестных источников" в настройках Android
2. Передайте APK на телефон
3. Запустите установку

## Структура APK

- **Бэкенд**: FastAPI + uvicorn (встроен в APK)
- **Фронтенд**: WebView с HTML/JS
- **База данных**: SQLite (хранится в памяти приложения)

## Отладка

```bash
buildozer android logcat  # Просмотр логов
buildozer android clean   # Очистка сборки
```
