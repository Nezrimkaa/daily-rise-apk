"""
Daily Rise - Простой лаунчер для Windows
Открывает приложение в браузере по умолчанию
"""

import webbrowser
import subprocess
import time
import sys
import os

def run_server():
    """Запуск сервера"""
    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
    )
    return server

def main():
    print("🌱 Daily Rise - Запуск...")
    print()
    
    # Запускаем сервер
    print("→ Запуск сервера...")
    server = run_server()
    
    # Ждём запуска
    time.sleep(3)
    
    # Открываем браузер
    print("→ Открытие приложения...")
    webbrowser.open('http://localhost:8000')
    
    print()
    print("✓ Приложение запущено!")
    print("  Сервер работает на http://localhost:8000")
    print()
    print("Нажми Ctrl+C для остановки сервера")
    
    try:
        server.wait()
    except KeyboardInterrupt:
        print("\n→ Остановка сервера...")
        server.terminate()
        print("✓ До свидания!")

if __name__ == '__main__':
    main()
