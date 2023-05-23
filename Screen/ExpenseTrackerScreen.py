from libs.kivymd_package import *

class ExpenseTrackerScreen(MDScreen):
    def __init__(self, **kwargs):
        super(ExpenseTrackerScreen, self).__init__(**kwargs)
        self.name = "Expense Tracker"
        self.add_widget(
            MDLabel(
                text="Notes",
                halign="center"
            ),
        )
        