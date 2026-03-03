"""
Daily Rise - Android App (Kivy + встроенный HTTP сервер)
Офлайн-режим: бэкенд работает локально на устройстве
"""
from kivy.app import App
from kivy.uix.webview import WebView
from kivy.clock import Clock
from kivy.logger import Logger
import threading
import http.server
import socketserver
import os
import sys

PORT = 8000

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Тихий HTTP обработчик без логов"""
    def log_message(self, format, *args):
        pass  # Отключаем логирование
    
    def do_GET(self):
        # Обслуживаем файлы из текущей директории
        return super().do_GET()

class DailyRiseApp(App):
    httpd = None
    
    def start_server(self):
        """Запуск локального HTTP сервера"""
        try:
            # Определяем путь к файлам
            if hasattr(sys, '_MEIPASS'):
                os.chdir(sys._MEIPASS)
            else:
                os.chdir(os.path.dirname(os.path.abspath(__file__)))
            
            # Создаём сервер
            socketserver.TCPServer.allow_reuse_address = True
            self.httpd = socketserver.TCPServer(("", PORT), QuietHandler)
            
            Logger.info(f'Daily Rise: Starting server on port {PORT}')
            self.httpd.serve_forever()
        except Exception as e:
            Logger.error(f'Daily Rise: Server error - {e}')
    
    def build(self):
        # Запускаем сервер в отдельном потоке
        server_thread = threading.Thread(target=self.start_server, daemon=True)
        server_thread.start()
        
        # Ждём запуска сервера
        Clock.schedule_once(self.load_webview, 2)
        
        # Возвращаем WebView
        webview = WebView()
        return webview
    
    def load_webview(self, dt):
        """Загрузка веб-приложения в WebView"""
        try:
            webview = self.root
            webview.load_url(f'http://localhost:{PORT}')
            Logger.info('Daily Rise: WebView loaded')
        except Exception as e:
            Logger.error(f'Daily Rise: WebView error - {e}')
    
    def on_stop(self):
        """Остановка сервера при закрытии"""
        if self.httpd:
            self.httpd.shutdown()
            Logger.info('Daily Rise: Server stopped')

if __name__ == '__main__':
    DailyRiseApp().run()
