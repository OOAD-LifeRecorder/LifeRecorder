from libs.kivymd_package import *
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, TwoLineRightIconListItem, IconRightWidget
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dialog import MDDialog

from datetime import datetime
import json

class NotesScreen(MDScreen):
    def __init__(self, **kwargs):
        super(NotesScreen, self).__init__(**kwargs)
        self.name = "Notes"
        self.notescreenmanager = NotesScreenManager()
        self.hp = NotesHomePage()
        self.notescreenmanager.add_widget(self.hp)
        self.ap = NotesAddPage(homepage = self.hp)
        self.notescreenmanager.add_widget(self.ap)
        self.add_widget(self.notescreenmanager)
        
    
class NotesHomePage(MDScreen):
    def __init__(self, **kwargs):
        super(MDScreen, self).__init__(**kwargs)
        self.name = "NotesHomepage"
        self.home_layout = MDGridLayout(cols=1)
        self.add_widget(self.home_layout)
        self.memo_list = MDList(id="memo_list")
        self.get_buttons()
        self.get_added_memo()

    def get_buttons(self):
        layout = FloatLayout(
            size_hint_y=None
        )
        buttons = [
            MDRaisedButton(
                text='ADD',
                pos_hint={"center_x": 0.5, "center_y": 0.5}, 
                on_release = self.turn_to_add_pages
            )
        ]
        for button in buttons:
            layout.add_widget(button)
        self.home_layout.add_widget(layout)
    
    def turn_to_add_pages(self, *kwargs):
        self.manager.current = 'NotesAddPage'

    def turn_to_delete_pages(self, *kwargs):
        self.manager.current = 'NotesDeletePage'


    def get_added_memo(self):
        scroll_view = MDScrollView() 
        if datamanager.all_data == []:  
            pass
        else:
            for m in datamanager.all_data:
                list_item = MemoItem(
                    text = m['TITLE'], 
                    secondary_text = m['CONTENTS'], 
                    size_hint_y=None, 
                    height=60,
                )
                self.memo_list.add_widget(list_item)
            scroll_view.add_widget(self.memo_list)
        self.home_layout.add_widget(scroll_view)


    
class MemoItem(TwoLineRightIconListItem):
    def __init__(self, **kwargs):
        super(MemoItem, self).__init__(**kwargs)
        self.id = "memo_item"
        self.delete_icon = IconRightWidget(
            icon = 'trash-can',
            on_release = self.delete_memo
        )
        self.add_widget(self.delete_icon)

    def delete_memo(self, _):
        self.parent.remove_widget(self) 
        datamanager.delete_memo(self)
        
class NotesAddPage(MDScreen):
    def __init__(self, **kwargs):
        super(MDScreen, self).__init__() # init 的 kwarg 改掉了
        self.name = "NotesAddPage"
        self.add_widget(self.get_buttons())
        self.TITLE = None
        self.CONTENTS = None
        self.add_widget(self.get_textinput())
        self.homepage = kwargs['homepage']
        self.title = ''
        self.contents = ''

    def get_buttons(self):
        layout = FloatLayout()
        buttons = [
            MDRaisedButton(
                text='ADD', 
                pos_hint={"center_x": 0.3, "center_y": 0.8}, 
                on_release = self.return_data
            ), 
            MDRaisedButton(
                text='CANCEL', 
                pos_hint={"center_x": 0.7, "center_y": 0.8}, 
                on_release = self.turn_to_homepage
            )
        ]
        for button in buttons:
            layout.add_widget(button)
        return layout
    
    def return_data(self, *kwargs):
        data = {}
        data['TITLE'] = self.title
        data['CONTENTS'] = self.contents
        if data['TITLE'] == "" and data['CONTENTS'] == "":
            self.dialog = MDDialog(
                text = "Two Inputs Are Neccessary",
                buttons = [
                    MDRaisedButton(
                    text = 'CONFIRM',
                    on_release = self.confirm_dialog
                    ), 
                    MDRaisedButton(
                    text = 'CANCEL',
                    on_release = self.cancel_dialog
                    )
                ]

            )
            self.dialog.open()
        else:
            datamanager.all_data.append(data)
            datamanager.edit_memo()
            self.TITLE.text = ''
            self.CONTENTS.text = ''

            list_item = MemoItem(
                text = data['TITLE'], 
                secondary_text = data['CONTENTS'], 
                size_hint_y=None, 
                height=60,
            )
            self.manager.get_screen("NotesHomepage").memo_list.add_widget(
                list_item
            )
            self.manager.current = 'NotesHomepage'
    def confirm_dialog(self, object):
        self.dialog.dismiss()

    def cancel_dialog(self, object):
        self.dialog.dismiss()
        self.manager.current = 'NotesHomepage'

    def turn_to_homepage(self, *kwargs):
        self.manager.current = 'NotesHomepage'
    
    def get_textinput(self):
        layout = MDBoxLayout(
                    orientation="vertical",
                    spacing="20dp",
                    adaptive_height=True,
                    pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.TITLE = MDTextField(text = '',
                        hint_text="Title",
                        helper_text="Enter your title",
                        multiline = True,
                        required = True
                    )

        self.CONTENTS = MDTextField(text = '',
                        hint_text="Contents",
                        helper_text="Enter your contents about this memo",
                        multiline = True,
                        required = True
                    )
        self.TITLE.bind(text = self.return_title)
        self.CONTENTS.bind(text = self.return_contents)
        layout.add_widget(self.TITLE)
        layout.add_widget(self.CONTENTS)
        return layout

    def return_title(self, instance, text):
        self.title = text

    def return_contents(self, instance, text):
        self.contents = text
    
class NotesScreenManager(MDScreenManager):
    def __init__(self, **kwargs):
        super(MDScreenManager, self).__init__(**kwargs)

class DataStorage():
    def __init__(self):
        self.rootpath = ".\memo\memos.json"
        self.all_data = []

    def edit_memo(self, **kwargs):
        with open(self.rootpath, 'w') as f:
            json.dump(self.all_data, f)

    def delete_memo(self, list_item):
        title = list_item.text
        contents = list_item.secondary_text
        for i in self.all_data:
            for num, (t, c) in enumerate(i.items()):
                if title == i['TITLE'] and contents== i['CONTENTS']:
                    self.all_data.pop(num)
                    self.edit_memo()
                    return


    def load_memo(self):
        with open(self.rootpath, 'r') as f:
            try:
                self.all_data = json.load(f)
            except:
                pass
            
datamanager = DataStorage()
datamanager.load_memo()



