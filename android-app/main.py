"""
Daily Rise - Android App (Kivy)
Офлайн-режим: бэкенд работает локально на устройстве
"""
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.logger import Logger
import subprocess
import time
import os
import sys

class DailyRiseApp(App):
    backend_process = None

    def start_backend(self):
        """Запуск сервера в фоне"""
        try:
            # Определяем путь к приложению
            if hasattr(sys, '_MEIPASS'):
                app_dir = sys._MEIPASS
            else:
                app_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Путь к базе данных - в директорию приложения Android
            db_path = os.path.join(app_dir, 'habits.db')
            
            # Запускаем uvicorn с правильным путём
            self.backend_process = subprocess.Popen(
                [sys.executable, '-m', 'uvicorn', 'app.main:app', 
                 '--host', '127.0.0.1', '--port', '8000'],
                cwd=app_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, 'DATABASE_URL': f'sqlite+aiosqlite:///{db_path}'}
            )
            Logger.info(f'Backend started with PID: {self.backend_process.pid}')
            time.sleep(3)
        except Exception as e:
            Logger.error(f'Failed to start backend: {e}')

    def build(self):
        # Запускаем сервер
        self.start_backend()

        # Создаём WebView с локальным сервером
        Clock.schedule_once(self.load_webview, 3)
        return Widget()

    def load_webview(self, dt):
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            
            # Создаём WebView через Intent
            intent = Intent(Intent.ACTION_VIEW, Uri.parse('http://127.0.0.1:8000'))
            PythonActivity.mActivity.startActivity(intent)
        except Exception as e:
            Logger.error(f'Failed to load webview: {e}')

    def on_stop(self):
        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process.wait()
            Logger.info('Backend stopped')

if __name__ == '__main__':
    DailyRiseApp().run()
