# 📱 Создание Android APK

## Способ 1: Через онлайн сервис (просто)

1. Открой https://pwabuilder.com
2. Введи URL: `https://твой-сайт.com` (нужен HTTPS!)
3. Нажми **"Build for Android"**
4. Скачай APK файл
5. Установи на телефон

---

## Способ 2: Через Bubblewrap (продвинуто)

### Требования:
- Java JDK 11+
- Android SDK
- Node.js 18+

### Инструкция:

```bash
# 1. Установи Bubblewrap
npm install -g @bubblewrap/cli

# 2. Перейди в папку android
cd habit_tracker/android

# 3. Инициализируй проект
bubblewrap init --manifest ../app/static/manifest.json

# 4. Собери APK
bubblewrap build

# APK будет в: android/android/app/build/outputs/apk/
```

---

## Способ 3: Через Termux (на телефоне)

1. Установи Termux из F-Droid
2. Запусти:
```bash
pkg install python nodejs
cd /sdcard/habit_tracker
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

3. Открой в браузере телефона: `http://localhost:8000`

---

## 🎯 Быстрый тест

1. Запусти приложение на ПК
2. Узнай IP компьютера (ipconfig)
3. Открой с телефона: `http://192.168.x.x:8000`
4. Нажми 📲 → "Добавить на главный экран"
