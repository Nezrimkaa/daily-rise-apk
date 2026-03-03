"""
Daily Rise - Android App (Kivy WebView)
Простой WebView для отображения веб-приложения
"""
from kivy.app import App
from kivy.uix.webview import WebView
from kivy.logger import Logger

class DailyRiseApp(App):
    def build(self):
        # WebView для загрузки веб-приложения
        # Загружаем с GitHub Pages или другого хостинга
        webview = WebView()
        
        # URL вашего веб-приложения (нужно разместить на GitHub Pages или хостинге)
        # Для офлайн-режима нужно включить файлы локально
        Logger.info('Daily Rise: Starting WebView')
        
        # Пока заглушка - нужно настроить URL
        webview.load_url('https://nezrimkaa.github.io/daily-rise-web/')
        
        return webview

if __name__ == '__main__':
    DailyRiseApp().run()
