from logging import Manager
from typing import Sized, Text
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
from VUT_ITU_backend.Database import *
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.list import MDList, ThreeLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

#inicializace databaze
db = Database()

class StartScreen(MDScreen):
    pass

class LoginScreen(MDScreen):
    pass

class EditorScreen(MDScreen):
    added = False

    def add(self):
        if EditorScreen.added == False:
            scroll_editor = ScrollView(size_hint_y=.5, pos_hint={"x":0, "y": .2}, do_scroll_x=False, do_scroll_y=True)
            EditorScreen.added = True

        lection_list = MDList()
        scroll_editor.add_widget(lection_list)
        self.add_widget(scroll_editor)
        

class LessonsScreen(MDScreen):
    def __init__(self) -> None:
        super().__init__()
        self.lections = db.getLections()
        self.name="lessons_screen"
        self.filter_value=""

    
    def print_data(self):
        scroll = ScrollView(size_hint_y=.55, pos_hint={"x":0, "y": 0}, do_scroll_x=False, do_scroll_y=True)
        label_lections = MDLabel(text="Seznam lekcí", font_size=45, size_hint=(1, .2), pos_hint= {'center_y':.9}, halign="center")
        self.filter_value = TextInput(size_hint= (.5, .1), pos_hint= {'x': 0,'center_y':.7})
        filter_button = MDRaisedButton(on_press=self.filter, text="filtrovat", pos_hint= {'x': .6,'center_y':.7}, size_hint= (.2, .1))
        checkbox = CheckBox(pos_hint= {'center_y':.6, 'center_x': .5}, size_hint=(.1, .1))
        my_lections = MDLabel(text="Moje lekce", font_size=20, size_hint=(.5, .1), pos_hint= {'center_y':.6}, halign="left")

        self.add_widget(filter_button)
        self.add_widget(label_lections)
        self.add_widget(my_lections)
        self.add_widget(self.filter_value)
        self.add_widget(checkbox)
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        for item in self.lections:
            self.lab = ThreeLineListItem(text= item['name'], secondary_text="item['author']", tertiary_text=item['instrument'])
            self.list_view.add_widget(self.lab)

        self.add_widget(scroll)


    def filter(self, obj):
        print("filter: " + self.filter_value.text)
        self.remove_widget(self.list_view)



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