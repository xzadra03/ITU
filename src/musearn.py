import kivy
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import GridLayout


class Musearn(MDApp):
    screen = Screen()
    def build(self):
        screen = Screen()
        logo = MDLabel(text="Musearn", halign="center", valign="center", font_style="H3")
        button_lessons = MDRaisedButton(text="Seznam lekci")
        button_editor = MDRaisedButton(text="Vytvoř lekci")
        button_songs = MDRaisedButton(text="Zahrej si")
        screen.add_widget(logo)
        screen.add_widget(button_lessons)
        screen.add_widget(button_editor)
        screen.add_widget(button_songs)
        return screen


if __name__ == "__main__":
    Musearn().run()