# 📱 Сборка APK для Daily Rise

## ✅ Что уже сделано:

1. **Ярлык на рабочем столе** — `Daily Rise.lnk` создан
2. **Офлайн-режим** — приложение работает локально
3. **Файлы для сборки APK** подготовлены в папке `android-app`

---

## 🚀 Сборка через WSL2 (Вариант 2)

### Шаг 1: Перезагрузите компьютер
WSL2 требует перезагрузки для активации.

### Шаг 2: Запустите сборку

**Способ A — через .bat файл:**
```
Дважды кликните на: android-app\BUILD_APK.bat
```

**Способ B — вручную в PowerShell:**
```powershell
wsl bash -c "/mnt/c/Users/Илья/habit_tracker/android-app/build_apk.sh"
```

### Шаг 3: Дождитесь завершения
- Первая сборка: **15-25 минут**
- Повторная: **3-5 минут**

### Шаг 4: Найдите готовый APK
```
android-app\bin\dailyrise-0.1-1-debug.apk
```

---

## 📲 Установка на телефон

1. Включите **"Неизвестные источники"** в настройках Android
2. Передайте APK на телефон
3. Запустите установку

---

## 🔧 Если что-то пошло не так

### Ошибка "WSL не найден"
```powershell
# Переустановите WSL
wsl --uninstall
wsl --install -d Ubuntu
# ПЕРЕЗАГРУЗИТЕ компьютер
```

### Ошибка при сборке
```powershell
# Очистите и запустите заново
wsl bash -c "cd /mnt/c/Users/Илья/habit_tracker/android-app && buildozer android clean && buildozer -v android debug"
```

### Посмотреть логи
```powershell
wsl bash -c "cat /mnt/c/Users/Илья/habit_tracker/android-app/.buildozer/android/platform/build-arm64-v8a/dists/habit_tracker__arm64-v8a/build/outputs/logs/build.log"
```

---

## 📋 Требования к системе

- Windows 10/11 (64-bit)
- Включена виртуализация в BIOS
- Свободно ~10 GB места на диске

---

## 🎯 Альтернатива: Google Colab

Если WSL не работает, используйте Google Colab:
1. Откройте `GOOGLE_COLAB_BUILD.ipynb` в браузере
2. Выполните ячейки по очереди
3. Скачайте готовый APK

Ссылка на Colab: https://colab.research.google.com/
