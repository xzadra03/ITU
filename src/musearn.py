import kivy
kivy.require('2.0.0')
from kivy.lang.builder import custom_callback
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.icon_definitions import md_icons
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file("musearn.kv")

class StartScreen(Screen):
    pass
 
class LoginScreen(Screen):
    pass

class EditorScreen(Screen):
    pass

class LessonsScreen(Screen):
    pass
 
 
screen_manager = ScreenManager()
screen_manager.add_widget(StartScreen(name="start_screen"))
screen_manager.add_widget(LoginScreen(name="login_screen"))
screen_manager.add_widget(EditorScreen(name="editor_screen"))
screen_manager.add_widget(LessonsScreen(name="lessons_screen"))


class Musearn(MDApp):
    def build(self):
        return screen_manager


if __name__ == "__main__":
    Musearn().run()