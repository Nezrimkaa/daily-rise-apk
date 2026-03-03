"""
Daily Rise - Android App (Kivy)
Офлайн-режим: простое Kivy приложение
"""
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20
        
        title = Label(
            text='🌱 Daily Rise',
            font_size='48sp',
            bold=True,
            size_hint=(1, 0.3)
        )
        
        subtitle = Label(
            text='Трекер привычек\\n\\nПриложение в разработке',
            font_size='24sp',
            size_hint=(1, 0.4)
        )
        
        self.add_widget(title)
        self.add_widget(subtitle)

class DailyRiseApp(App):
    def build(self):
        Logger.info('Daily Rise: Starting app')
        return MainScreen()

if __name__ == '__main__':
    DailyRiseApp().run()
