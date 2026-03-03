"""
Daily Rise - Desktop приложение
Запускает сервер и открывает приложение в окне
"""

import webview
import threading
import time
import sys
import os

# Добавляем родительскую директорию в path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_server():
    """Запуск FastAPI сервера в отдельном потоке"""
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="warning"
    )

def create_app():
    """Создание и запуск приложения"""
    
    # Запускаем сервер в фоне
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Ждём запуска сервера
    time.sleep(2)
    
    # Создаём окно приложения
    window = webview.create_window(
        title='🌱 Daily Rise — Трекер привычек',
        url='http://127.0.0.1:8000',
        width=1200,
        height=800,
        min_size=(400, 600),
        resizable=True,
        fullscreen=False,
        background_color='#f5f5f7'
    )
    
    # Запускаем приложение
    webview.start()

if __name__ == '__main__':
    create_app()
