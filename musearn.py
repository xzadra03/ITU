from typing import Text
import kivy
from kivymd.uix import screen
from kivymd.uix import button
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
from VUT_ITU_backend import Database
from kivy.uix.recycleview import RecycleView


class StartScreen(MDScreen):
    pass

class LoginScreen(MDScreen):
    pass

class EditorScreen(MDScreen):
    pass


class LessonsScreen(MDScreen):
    def __init__(self) -> None:
        super().__init__()
        self.lections = ["Prvek1", "Prvek2", "Prvek3", "Prvek4", "Prvek5", "Prvek6", "Prvek1", "Prvek2", "Prvek3", "Prvek4", "Prvek5", "Prvek6"]
        self.name="lessons_screen"

    
    def print_data(self):
        i = 7
        for item in self.lections:
            i = i - 1
            pos_x = .5
            pos_y = "." + str(i)
            lab = MDLabel(text=str(item), font_size=25, size_hint=(1, .1), pos_hint= {"center_y":.7, "center_x":pos_x}, halign='left', line_color= (0, 0, 0, 1))
            btn = MDRaisedButton(text="Zobrazit", pos_hint= {"center_y":.7, "center_x":pos_x})
            self.add_widget(btn)
            self.add_widget(lab)

 

class Musearn(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        Builder.load_file("musearn.kv")
        screen_manager.add_widget(StartScreen(name="start_screen"))
        screen_manager.add_widget(LoginScreen(name="login_screen"))
        screen_manager.add_widget(EditorScreen(name="editor_screen"))
        ls_screen = LessonsScreen()
        screen_manager.add_widget(ls_screen)
        return screen_manager


if __name__ == "__main__":
    Musearn().run()