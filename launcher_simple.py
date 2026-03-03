"""
Daily Rise - Лаунчер приложения
Просто открывает браузер с приложением
"""

import webbrowser
import subprocess
import time
import sys
import os

# Получаем директорию приложения
app_dir = os.path.dirname(os.path.abspath(__file__))
venv_python = os.path.join(app_dir, 'venv', 'Scripts', 'python.exe')

def main():
    # Проверяем venv
    if not os.path.exists(venv_python):
        print("Ошибка: виртуальное окружение не найдено!")
        print("Запустите build_app.bat для установки.")
        input()
        return
    
    # Запускаем сервер
    subprocess.Popen(
        [venv_python, '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000'],
        cwd=app_dir,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    
    # Ждём запуска
    time.sleep(3)
    
    # Открываем браузер
    webbrowser.open('http://127.0.0.1:8000')

if __name__ == '__main__':
    main()
