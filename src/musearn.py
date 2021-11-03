from typing import Text
import kivy
from kivy.app import App
from kivy.uix.label import Label

class Musearn(App):
    def build(self):
        return Label(Text = "ITU app")

if __name__ == "__main__":
    Musearn().run()

