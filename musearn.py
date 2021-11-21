#_________________________________
#|                                |
#|    Kivy version of Musearn     |
#|       author: Jan Zadrapa      |
#|      project created for ITU   |
#|         BUT FIT 11/2021        |
#|                                |
#|________________________________|

#importy
from functools import partial
from logging import Manager
import kivy
from kivymd.uix import label
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
from VUT_ITU_backend.BlockList import *
from VUT_ITU_backend.Constants import *
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import MDList, OneLineListItem, ThreeLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image
import os
import inspect

#inicializace databaze
db = Database()
#inicializace obrazovek
screen_manager = ScreenManager()
#nastaveni cesty k souborum
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

class Content(BoxLayout):
    pass

#trida startovni obrazovky
class StartScreen(MDScreen):
    pass

#trida prihlasovaci obrazovky
class LoginScreen(MDScreen):
    log_user = None
    reg_user = None
    wrong_password = None
    username_input = "default"

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
            else:
                LoginScreen.wrong_password = MDLabel(text="Spatne heslo", font_size=30, size_hint=(1, .2), pos_hint= {'center_y':.1}, halign="center")
                self.add_widget(LoginScreen.wrong_password)

    def clean(self):
        if LoginScreen.log_user is not None:
            self.remove_widget(LoginScreen.log_user)
        if LoginScreen.reg_user is not None:
            self.remove_widget(LoginScreen.reg_user)
        if LoginScreen.wrong_password is not None:
            self.remove_widget(LoginScreen.wrong_password)
        
        self.ids.username.text = ""
        self.ids.password.text = ""

#trida pro editor
class EditorScreen(MDScreen):
    section_list = []

    def add(self):
        #print("pridavam")
        self.list_view = MDList()
        self.scroll_editor = ScrollView(size_hint_y=.6, pos_hint={"x":0, "y": .2}, do_scroll_x=False, do_scroll_y=True)
        self.scroll_editor.add_widget(self.list_view)
        self.add_widget(self.scroll_editor)

    def add_label(self):
        print("Pridej label")
        self.section_list.append("paragraph")
        self.label_input = TextInput(text = "Label" ,size_hint= (.6, .2), pos_hint= (None, None))
        self.delete_button = MDRoundFlatIconButton(icon="delete", text="smazat", pos_hint=(.8, None), size_hint=(.2, .1), on_press=self.delete_label)
        self.list_view.add_widget(self.label_input)
        self.list_view.add_widget(self.delete_button)

    def delete_label(self, obj):
        print("mazu_label")
        self.section_list.remove("paragraph")
        self.list_view.remove_widget(self.delete_button)
        self.list_view.remove_widget(self.label_input)

    def add_image(self):
        print("Pridej image")
        self.section_list.append("image")
        self.image = Image(source="VUT_ITU_backend/img/melon.jpg")
        self.delete_button = MDRoundFlatIconButton(icon="delete", text="smazat", pos_hint=(None, None), size_hint=(.2, .1))
        self.list_view.add_widget(self.image)
        self.list_view.add_widget(self.delete_button)

    def add_video(self):
        print("Pridej video")

    def add_title(self):
        print("Pridej title")
        self.section_list.append("title")
        self.title_input = TextInput(text = "Title" ,size_hint= (1, .2), pos_hint= (None, None))
        self.delete_button = MDRoundFlatIconButton(icon="delete", text="smazat", pos_hint=(.8, None), size_hint=(.2, .1), on_press=self.delete_title)
        self.list_view.add_widget(self.title_input)
        self.list_view.add_widget(self.delete_button)

    def delete_title(self, obj):
        print("mazu_title")
        self.section_list.remove("title")
        self.list_view.remove_widget(self.delete_button)
        self.list_view.remove_widget(self.title_input)

    def delete(self):
        print("mazu")
        self.remove_widget(self.scroll_editor)

    def save_lection_popup(self):
        self.dialog = MDDialog(
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDRaisedButton(text="CANCEL", on_press=self.close_dialog),
                    MDRaisedButton(text="OK", on_press=self.save_lection),
                ],
            )
        self.dialog.open()
    
    def close_dialog(self, obj):
        self.dialog.dismiss(force=True)

    def save_lection(self, obj):
        self.blocks = BlockList()

        for section in EditorScreen.section_list:
            if section == BlockType.title:
                print(section)
                #title = section
                self.blocks.addBlock("title","Toto je pokus")
            
            if section == BlockType.paragraph:
                print(section)
            
            # image section
            if section == BlockType.image: 
                pass       
                #self.blocks.addBlock(section.type.name, str(section.path))
            
            # video section
            if section == BlockType.video:
                pass
               # self.blocks.addBlock(section.type.name, str(section.path))



        lection_name = self.dialog.content_cls.ids.name.text
        instrument = self.dialog.content_cls.ids.instrument.text
        difficulty = int(self.dialog.content_cls.ids.difficulty.text)
        db.createLection(lection_name, LoginScreen.username_input, instrument, difficulty, self.blocks.jsonList)
        print("Ulozeno")
        self.dialog.dismiss(force=True)
        self.delete()

#trida pro prohlizeci obrazovku
class LessonsScreen(MDScreen):
    lection_to_view = {"id": None, "name": None}

    def __init__(self) -> None:
        super().__init__()
        self.lections = db.getLections()
        self.name="lessons_screen"
        self.filter_value=""

    
    def print_data(self):
        self.scroll = ScrollView(size_hint_y=.55, pos_hint={"x":0, "y": 0}, do_scroll_x=False, do_scroll_y=True)
        self.label_lections = MDLabel(text="Seznam lekcí", font_size=45, size_hint=(1, .2), pos_hint= {'center_y':.9}, halign="center")
        self.filter_value = TextInput(size_hint= (.5, .1), pos_hint= {'x': 0,'center_y':.7})
        self.filter_button = MDRaisedButton(on_press=self.filter, text="filtrovat", pos_hint= {'x': .6,'center_y':.7}, size_hint= (.2, .1))
        self.my_lections = MDLabel(text="Moje lekce", font_size=20, size_hint=(.5, .1), pos_hint= {'center_y':.6}, halign="left")

        self.add_widget(self.filter_button)
        self.add_widget(self.label_lections)
        self.add_widget(self.my_lections)
        self.add_widget(self.filter_value)
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        i = 0
        for item in self.lections:
            self.lab = ThreeLineListItem(text= item['name'], secondary_text=item['author'], tertiary_text=item['instrument'], on_press=partial(self.view_lection, item["name"]))
            self.list_view.add_widget(self.lab)
            i = i + 1

        self.add_widget(self.scroll)

    #filtrovani
    def filter(self, obj):
        if self.filter_value.text == "":
            self.remove_widget(self.scroll)
            self.scroll.remove_widget(self.list_view)
            self.list_view = MDList()
            for item in self.lections:
                self.lab = ThreeLineListItem(text= item['name'], secondary_text=item['author'], tertiary_text=item['instrument'], on_press=partial(self.view_lection, item["name"]))
                self.list_view.add_widget(self.lab)

            self.scroll.add_widget(self.list_view)
            self.add_widget(self.scroll)
        else:
            self.remove_widget(self.scroll)
            self.scroll.remove_widget(self.list_view)
            self.list_view = MDList()
            for item in self.lections:
                if item['name'] == self.filter_value.text or item['author'] == self.filter_value.text or item['instrument'] == self.filter_value.text:
                    self.lab = ThreeLineListItem(text= item['name'], secondary_text=item['author'], tertiary_text=item['instrument'], on_press=partial(self.view_lection, item["name"]))
                    self.list_view.add_widget(self.lab)

            self.scroll.add_widget(self.list_view)
            self.add_widget(self.scroll)

    def filter_user_checked(self, instance):
        if instance is True:
            self.remove_widget(self.scroll)
            self.scroll.remove_widget(self.list_view)
            self.list_view = MDList()
            for item in self.lections:
                if item['name'] == LoginScreen.username_input:
                    self.lab = ThreeLineListItem(text= item['name'], secondary_text=item['author'], tertiary_text=item['instrument'], on_press=partial(self.view_lection, item["name"]))
                    self.list_view.add_widget(self.lab)

            self.scroll.add_widget(self.list_view)
            self.add_widget(self.scroll)
        else:
            self.remove_widget(self.scroll)
            self.scroll.remove_widget(self.list_view)
            self.list_view = MDList()
            for item in self.lections:
                self.lab = ThreeLineListItem(text= item['name'], secondary_text=item['author'], tertiary_text=item['instrument'], on_press=partial(self.view_lection, item["name"]))
                self.list_view.add_widget(self.lab)

            self.scroll.add_widget(self.list_view)
            self.add_widget(self.scroll)

    def delete(self):
        #print("mazu")
        self.remove_widget(self.scroll)
        self.remove_widget(self.filter_button)
        self.remove_widget(self.label_lections)
        self.remove_widget(self.my_lections)


    def view_lection(self, obj, name):
        LessonsScreen.lection_to_view["name"] = obj
        screen_manager.current = "view_screen"


class ViewScreen(MDScreen):
    lect = db.getLections()
    located = False
    button_edit = None
    content = ""

    def view(self):
        self.lect_view = MDList()
        self.scroll_view = ScrollView(size_hint_y=.8, pos_hint={"x":0, "y": 0}, do_scroll_x=False, do_scroll_y=True)
        self.scroll_view.add_widget(self.lect_view)
        self.add_widget(self.scroll_view)
        i = 0
        for item in ViewScreen.lect:
            if LessonsScreen.lection_to_view["name"] == item["name"]:
                ViewScreen.located = True
                LessonsScreen.lection_to_view["id"] = i
            i = i + 1

        if ViewScreen.located is True:
            if LoginScreen.username_input == self.lect[int(LessonsScreen.lection_to_view["id"])]["author"]:
                self.button_edit = MDRaisedButton(text="Editovat", pos_hint={"x": 0, "y":0.9}, on_press=self.change_to_editor)
                self.add_widget(self.button_edit)
            
            for key in ViewScreen.lect:
                if key["name"] == LessonsScreen.lection_to_view["name"]:
                    self.label_lection = MDLabel(text=self.lect[int(LessonsScreen.lection_to_view["id"])]["name"], font_size=42, pos_hint={"x": 0, "y":0.9}, size_hint=(1, .1), halign="center")
                    self.add_widget(self.label_lection)
                    self.label_lect_author = OneLineListItem(text="Autor: " + self.lect[int(LessonsScreen.lection_to_view["id"])]["author"])
                    self.lect_view.add_widget(self.label_lect_author)
                    self.label_lect_instrument = OneLineListItem(text="Nástroj: " + self.lect[int(LessonsScreen.lection_to_view["id"])]["instrument"])
                    self.lect_view.add_widget(self.label_lect_instrument)
                    self.label_lect_diff = OneLineListItem(text="Obtížnost: " + str(self.lect[int(LessonsScreen.lection_to_view["id"])]["difficulty"]))
                    self.lect_view.add_widget(self.label_lect_diff)
                    self.label_lect_rating = OneLineListItem(text="Hodnocení: " + str(self.lect[int(LessonsScreen.lection_to_view["id"])]["rating"]))
                    self.lect_view.add_widget(self.label_lect_rating)
                    self.label_lect_date = OneLineListItem(text="Datum vytvoření:" + str(self.lect[int(LessonsScreen.lection_to_view["id"])]["timestamp"]))
                    self.lect_view.add_widget(self.label_lect_date)

                    #ted nacist samotny content lekce
                    for block in key["blocks"]:
                        if block["blockType"] == "title":
                            ViewScreen.content = block["content"]
                            self.print_title()
                        elif block["blockType"] == "paragraph":
                            ViewScreen.content = block["content"]
                            self.print_paragraph()
                        elif block["blockType"] == "image":
                            ViewScreen.content = block["content"]
                            self.print_image()
                        elif block["blockType"] == "video":
                            ViewScreen.content = block["content"]
                            self.print_video()

                    #print("Lekce vytistena")


    def print_title(self):
        self.label_lection_title = MDLabel(text=ViewScreen.content, font_size=30, size_hint=(1, None))
        self.lect_view.add_widget(self.label_lection_title)

    def print_paragraph(self):
        self.label_lection_p = MDLabel(text=ViewScreen.content, font_size=30, size_hint=(1, None))
        self.lect_view.add_widget(self.label_lection_p)

    def print_image(self):
        #zkus najit lokalne jinak stahni z databaze
        if not os.path.exists(currentdir + "/images"):
            os.mkdir(currentdir + "/images/")
        file_path = currentdir + "/images/" + str(ViewScreen.content)
        if not os.path.exists(file_path):
            db.downloadFile(ViewScreen.content, currentdir + "/images/" + ViewScreen.content)
    
        label_lection_test = MDLabel(text="obrazek", size_hint=(1, None))
        self.image_lection = Image(source=file_path,  allow_stretch=True, keep_ratio=True)
        self.lect_view.add_widget(label_lection_test)
        label_lection_test.add_widget(self.image_lection)

    def print_video(self):
        self.label_lection_video = MDLabel(text="Video", size_hint=(1, None))
        self.lect_view.add_widget(self.label_lection_video)

    def delete(self):
        self.remove_widget(self.scroll_view)
        self.remove_widget(self.label_lection)
        if self.button_edit is not None:
            self.remove_widget(self.button_edit)

    def change_to_editor(self, obj):
        self.delete()
        screen_manager.current = "editor_screen"



#hlavni trida aplikace
class Musearn(MDApp):
    def build(self):
        #z nejakeho duvodu se mi to s timto radkem nacitalo dvakrat
        #Builder.load_file("musearn.kv")
        screen_manager.add_widget(StartScreen(name="start_screen"))
        screen_manager.add_widget(ViewScreen(name="view_screen"))
        screen_manager.add_widget(LoginScreen(name="login_screen"))
        screen_manager.add_widget(EditorScreen(name="editor_screen"))
        ls_screen = LessonsScreen()
        screen_manager.add_widget(ls_screen)
        return screen_manager


if __name__ == "__main__":
    Musearn().run()