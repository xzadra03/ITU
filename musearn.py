#_________________________________
#|                                |
#|    Kivy version of Musearn     |
#|       author: Jan Zadrapa      |
#|      project created for ITU   |
#|         BUT FIT 11/2021        |
#|                                |
#|________________________________|

#importy
from logging import Manager
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
from VUT_ITU_backend.Database import Database
from VUT_ITU_backend import *
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import MDList, ThreeLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image

#inicializace databaze
db = Database()

class Content(BoxLayout):
    pass

#trida startovni obrazovky
class StartScreen(MDScreen):
    pass

#trida prihlasovaci obrazovky
class LoginScreen(MDScreen):
    log_user = None
    reg_user = None
    username_input = ""

    def login(self):
        LoginScreen.username_input = self.ids.username.text
        password_input = self.ids.password.text

        if password_input is None or LoginScreen.username_input is None:
            return
        if db.doesUserExist(LoginScreen.username_input) is False:
            if db.createUser(LoginScreen.username_input, password_input) is True:
                LoginScreen.reg_user = MDLabel(text="Registrovan", font_size=30, size_hint=(1, .2), pos_hint= {'center_y':.1}, halign="center")
                self.add_widget(LoginScreen.reg_user)
        else:
            if db.loginUser(LoginScreen.username_input, password_input) is True:
                LoginScreen.log_user = MDLabel(text="Prihlasen", font_size=30, size_hint=(1, .2), pos_hint= {'center_y':.1}, halign="center")
                self.add_widget(LoginScreen.log_user)
                user = MDLabel(text="uzivatel: " + LoginScreen.username_input, font_size=30, size_hint=(.3, .1), pos_hint= {'center_y':.9}, halign="left")
                self.add_widget(user)

    def clean(self):
        if LoginScreen.log_user is not None:
            self.remove_widget(LoginScreen.log_user)
        if LoginScreen.reg_user is not None:
            self.remove_widget(LoginScreen.reg_user)
        
        self.ids.username.text = ""
        self.ids.password.text = ""

#trida pro editor
class EditorScreen(MDScreen):
    def add(self):
        #print("pridavam")
        self.list_view = MDList()
        self.scroll_editor = ScrollView(size_hint_y=.6, pos_hint={"x":0, "y": .2}, do_scroll_x=False, do_scroll_y=True)
        self.scroll_editor.add_widget(self.list_view)
        self.add_widget(self.scroll_editor)

    def add_label(self):
        print("Pridej label")
        self.label_input = TextInput(text = "Label" ,size_hint= (.8, .2), pos_hint= (None, None))
        #self.delete_button = MDRoundFlatIconButton(icon="delete", text="smazat", pos_hint=(None, None), size_hint=(.2, .1))
        self.list_view.add_widget(self.label_input)
        #self.list_view.add_widget(self.delete_button)

    # def delete_label(self):
    #     print("mazu_label")
    #     self.remove_widget(self.label_input)

    def add_image(self):
        print("Pridej image")
        self.image = Image(source="VUT_ITU_backend/img/melon.jpg")
       # self.delete_button = MDRoundFlatIconButton(icon="delete", text="smazat", pos_hint=(None, None), size_hint=(.2, .1))
        self.list_view.add_widget(self.image)
        #self.list_view.add_widget(self.delete_button)

    def add_video(self):
        print("Pridej video")

    def add_title(self):
        print("Pridej title")
        self.title_input = TextInput(text = "Title" ,size_hint= (1, .2), pos_hint= (None, None))
        self.list_view.add_widget(self.title_input)

    def delete(self):
        print("mazu")
        self.remove_widget(self.scroll_editor)

    def save_lection_popup(self):
        print("Ukladam")
        self.dialog = MDDialog(title="Additional info:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDRaisedButton(text="CANCEL"),
                    MDRaisedButton(text="OK"),
                ],
            )
        self.dialog.open()
    
    def save_lection(self):
        print("Ulozeno")
        pass


#trida pro prohlizeci obrazovku
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
            self.lab = ThreeLineListItem(text= item['name'], secondary_text=item['author'], tertiary_text=item['instrument'])
            self.list_view.add_widget(self.lab)

        self.add_widget(scroll)


    def filter(self, obj):
        print("filter: " + self.filter_value.text)
        self.remove_widget(self.list_view)


#hlavni trida aplikace
class Musearn(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        #z nejakeho duvodu se mi to s timto radkem nacitalo dvakrat
        #Builder.load_file("musearn.kv")
        screen_manager.add_widget(StartScreen(name="start_screen"))
        screen_manager.add_widget(LoginScreen(name="login_screen"))
        screen_manager.add_widget(EditorScreen(name="editor_screen"))
        ls_screen = LessonsScreen()
        screen_manager.add_widget(ls_screen)
        return screen_manager


if __name__ == "__main__":
    Musearn().run()