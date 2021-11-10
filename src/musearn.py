import kivy
kivy.require('2.0.0')
from kivy.lang.builder import custom_callback
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import GridLayout
from kivymd.icon_definitions import md_icons
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


Builder.load_file("musearn.kv")


class StartScreen(Screen):
    pass
 
class LoginScreen(Screen):
    pass
 
 
screen_manager = ScreenManager()
screen_manager.add_widget(StartScreen(name="start_screen"))
screen_manager.add_widget(LoginScreen(name="login_screen"))
 
class Musearn(MDApp):
    def build(self):
        return screen_manager
 
sample_app = Musearn()
sample_app.run()



# class Musearn(MDApp):
#     def ahoj(self, obj):
#         print("ahoj")


#     def build(self):
#         screen = Screen()
#         logo = MDLabel(text="Musearn", size_hint =(1, .2), pos_hint = {'center_y':.9}, halign = "center", font_style="H3")
#         button_lessons = MDRaisedButton(text="Seznam lekcí", font_style = "H4", size_hint = (1, .4), pos_hint ={'center_y':.6})
#         button_editor = MDRaisedButton(text="Vytvoř lekci", font_style = "H4" ,size_hint = (1, .4), pos_hint ={'center_y':.2})
#         button_login = MDRaisedButton(text="Prihlaseni", pos_hint = {'center_y':.97, 'center_x':.9}, on_press = self.ahoj)

#         screen.add_widget(logo)
#         screen.add_widget(button_lessons)
#         screen.add_widget(button_editor)
#         screen.add_widget(button_login)
#         return screen


# if __name__ == "__main__":
#     Musearn().run()