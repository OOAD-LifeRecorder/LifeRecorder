from libs.kivymd_package import *
from kivymd.uix.widget import MDWidget
from kivy.graphics import *
from kivy.metrics import *

class WeekTab(MDBoxLayout):
    def __init__(self, ref, text, active=False, **kwargs):
        super().__init__(**kwargs)
        self.active = active
        self.ref = ref
        self.text = text
        self.orientation="vertical"
        self.__add_date_label()
        self.__add_separator()

    def __add_date_label(self):
        if self.active:
            text = f"[color=36454F]{self.text}[/color]"
        else:
            text = f"[color=D3D3D3]{self.text}[/color]"
        self.label = MDLabel(
            text=f"[ref={self.ref}]{text}[/ref]",
            halign="center",
            markup=True,
            bold=True
        )
        self.add_widget(self.label)

    def __add_separator(self):
        if self.active:
            self.separator = ActiveSeparator(size_hint_y=None, height=dp(2))
        else:
            self.separator = Separator(size_hint_y=None, height=dp(2))
        self.add_widget(self.separator)

    def change_active_state(self):
        if not self.active:
            self.label.text = self.label.text.replace('D3D3D3', '36454F')
            self.remove_widget(self.separator)
            self.separator = ActiveSeparator(size_hint_y=None, height=dp(2))
            self.add_widget(self.separator)
        else:
            self.label.text = self.label.text.replace('36454F', 'D3D3D3')
            self.remove_widget(self.separator)
            self.separator = Separator(size_hint_y=None, height=dp(2))
            self.add_widget(self.separator)
        self.active = not self.active

class Separator(MDWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(211/256, 211/256, 211/256, .5)
            self.rect = Rectangle(
                pos=self.pos, size=self.size)
 
            self.bind(pos = self.update_rect,
                  size = self.update_rect)
 
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ActiveSeparator(MDWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(253/256, 218/256, 13/256, 1)
            self.rect = Rectangle(
                pos=self.pos, size=self.size)
 
            self.bind(pos = self.update_rect,
                  size = self.update_rect)
 
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size