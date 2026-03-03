# 🌱 Daily Rise — Трекер привычек

Приложение для отслеживания привычек с поддержкой:
- 💻 Desktop (Windows/Mac/Linux)
- 📱 Android (APK)
- 🌐 Web (браузер)

---

## 🚀 Быстрый старт

### 1. Установка
```bash
# Запустить установщик
install.bat
```

### 2. Запуск
```bash
# Запустить приложение
start_app.bat
```

Доступные режимы:
1. **В браузере** — открывается http://localhost:8000
2. **Desktop приложение** — отдельное окно
3. **Только сервер** — для доступа с телефона

---

## 📱 Установка на телефон

### Через браузер:
1. Открой http://твой-ip:8000 с телефона
2. Нажми на 📲 в шапке
3. Следуй инструкции

### APK файл:
```bash
# Linux/Mac
./build_apk.sh

# Или через онлайн сервис:
# 1. https://pwabuilder.com
# 2. Введи URL
# 3. Скачай APK
```

---

## 💻 Desktop приложение

### Требования:
- Python 3.10+
- pip install pywebview

### Запуск:
```bash
python desktop_app.py
```

Или через `start_app.bat` → режим 2

---

## 🌐 Доступ с других устройств

1. Запусти сервер:
   ```bash
   start_app.bat → режим 3
   ```

2. Открой с телефона/планшета:
   ```
   http://твой-ip:8000
   ```

3. IP компьютера:
   ```bash
   ipconfig  # Windows
   ifconfig  # Linux/Mac
   ```

---

## 📦 Сборка приложений

### Windows (.exe):
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=app/static/icon.ico desktop_app.py
```

### Android (.apk):
```bash
# Способ 1: Buildozer (Linux)
./build_apk.sh

# Способ 2: PWABuilder (онлайн)
# https://pwabuilder.com
```

---

## 🛠️ Технологии

- **Frontend**: HTML, CSS, JavaScript (PWA)
- **Backend**: FastAPI (Python)
- **БД**: SQLite + SQLAlchemy
- **Desktop**: pywebview
- **Mobile**: TWA (Trusted Web App)

---

## 📝 Структура

```
habit_tracker/
├── app/                    # Backend + Frontend
│   ├── static/            # HTML, CSS, JS
│   ├── routers/           # API endpoints
│   ├── main.py            # FastAPI приложение
│   └── ...
├── electron/              # Electron версия
├── android/               # Android версия
├── desktop_app.py         # Desktop launcher
├── start_app.bat          # Запуск (Windows)
└── install.bat            # Установка (Windows)
```

---

## 🔐 Данные

Все данные хранятся локально в `habits.db`

Для сброса:
```bash
del habits.db  # Windows
rm habits.db   # Linux/Mac
```

---

**Создавай привычки. Достигай целей.** 🎯
