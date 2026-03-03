# 📦 Сборка приложений Daily Rise

## 🖥️ Desktop приложение (Electron)

### Требования
- Node.js 18+
- Python 3.10+

### Установка и запуск
```bash
# Перейти в папку electron
cd electron

# Установить зависимости
npm install

# Запустить в режиме разработки
npm start

# Собрать установщики для Windows/Mac/Linux
npm run build
```

После сборки в папке `electron/dist` появятся:
- `.exe` — для Windows
- `.dmg` — для Mac
- `.AppImage` — для Linux

---

## 📱 Android приложение (APK)

### Требования
- Node.js 18+
- Java JDK 11+
- Android SDK

### Способ 1: Bubblewrap (рекомендуется)

```bash
# Перейти в папку android
cd android

# Установить зависимости
npm install

# Инициализировать проект (первый раз)
npm run init

# Собрать APK
npm run build
```

APK файл будет в `android/android/app/build/outputs/apk/`

### Способ 2: Через онлайн сервис

1. Открой https://pwabuilder.com
2. Введи URL: `http://твой-ip:8000`
3. Нажми "Build for Android"
4. Скачай APK файл

---

## 🚀 Быстрый старт

### Для тестирования на телефоне:
```bash
# Запустить сервер
cd ..
venv\Scripts\activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Для desktop приложения:
```bash
cd electron
npm install
npm start
```

---

## 📝 Примечания

- Для Android APK нужен HTTPS (кроме localhost)
- Для тестирования на телефоне используй ngrok:
  ```bash
  ngrok http 8000
  ```
- Electron приложение включает встроенный сервер
