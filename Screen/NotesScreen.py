from libs.kivymd_package import *

class NotesScreen(MDScreen):
    def __init__(self, **kwargs):
        super(NotesScreen, self).__init__(**kwargs)
        self.name = "Notes"
        self.add_widget(
            MDLabel(
                text="Notes",
                halign="center"
            ),
        )
        