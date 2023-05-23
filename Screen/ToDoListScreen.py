from libs.kivymd_package import *

class ToDoListScreen(MDScreen):
    def __init__(self, **kwargs):
        super(ToDoListScreen, self).__init__(**kwargs)
        self.name = "To-Do List"
        self.add_widget(
            MDLabel(
                text="To-Do List",
                halign="center"
            ),
        )
        