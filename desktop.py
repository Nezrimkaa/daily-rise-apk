"""
Daily Rise - Приложение с окном (без pywebview)
Использует встроенный в Windows WebView2
"""
import sys
import os
import subprocess
import time
import threading

app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

def start_server():
    """Запуск сервера"""
    python = os.path.join(app_dir, 'venv', 'Scripts', 'python.exe')
    if not os.path.exists(python):
        python = sys.executable
    
    subprocess.Popen(
        [python, '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000'],
        cwd=app_dir,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    time.sleep(3)

def create_app():
    """Создаём окно"""
    try:
        # Пробуем pywebview
        import webview
        
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        window = webview.create_window(
            title='🌱 Daily Rise',
            url='http://127.0.0.1:8000',
            width=1280,
            height=800,
            min_size=(400, 600),
            background_color='#f5f5f7'
        )
        
        webview.start()
        
    except ImportError:
        # Если нет pywebview - используем edgehtml (Windows)
        try:
            import webview
            server_thread = threading.Thread(target=start_server, daemon=True)
            server_thread.start()
            window = webview.create_window(
                title='🌱 Daily Rise',
                url='http://127.0.0.1:8000',
                width=1280,
                height=800,
                gui='edgechromium'
            )
            webview.start()
        except:
            # Последняя попытка - просто браузер
            print("Opening in browser...")
            import webbrowser
            server_thread = threading.Thread(target=start_server, daemon=True)
            server_thread.start()
            webbrowser.open('http://127.0.0.1:8000')
            print("App opened in browser. Keep this window open.")
            input("Press Enter to exit...")

if __name__ == '__main__':
    create_app()
