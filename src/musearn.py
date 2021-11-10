import kivy
kivy.require('2.0.0')
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

class StartScreen(MDScreen):
    pass

class LoginScreen(MDScreen):
    pass

class EditorScreen(MDScreen):
    pass

class LessonsScreen(MDScreen):
    #musim nacist veci z databaze lekci
    print("ahoj")
    pass
 

class Musearn(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        Builder.load_file("musearn.kv")
        screen_manager.add_widget(StartScreen(name="start_screen"))
        screen_manager.add_widget(LoginScreen(name="login_screen"))
        screen_manager.add_widget(EditorScreen(name="editor_screen"))
        screen_manager.add_widget(LessonsScreen(name="lessons_screen"))
        return screen_manager


if __name__ == "__main__":
    Musearn().run()