"""
Daily Rise - Desktop приложение
Создаёт окно с приложением
"""

import webview
import threading
import time
import sys
import os
import subprocess

# Добавляем путь к приложению
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

def run_server():
    """Запуск FastAPI сервера"""
    # Ищем Python в venv
    python_exe = os.path.join(app_dir, 'venv', 'Scripts', 'python.exe')
    if not os.path.exists(python_exe):
        python_exe = sys.executable
    
    subprocess.Popen(
        [python_exe, '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000'],
        cwd=app_dir,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    
    # Ждём запуска сервера
    time.sleep(3)

def create_window():
    """Создание окна приложения"""
    
    window = webview.create_window(
        title='🌱 Daily Rise',
        url='http://127.0.0.1:8000',
        width=1280,
        height=800,
        min_size=(400, 600),
        resizable=True,
        fullscreen=False,
        background_color='#f5f5f7',
        text_select=True
    )
    
    webview.start()

if __name__ == '__main__':
    # Запускаем сервер в фоне
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Создаём окно
    create_window()
