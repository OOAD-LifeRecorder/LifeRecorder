from kivymd.uix.button import MDIconButton, MDFloatingActionButtonSpeedDial
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.properties import DictProperty
ExpenseTrackerScreenKV = '''
#:import rgba kivy.utils.get_color_from_hex
<ExpenseTrackerScreen>:

<SwitchMode>:
    id: switch_mode
    data: self.data
    anchor:"right"
    pos_hint: {"right": 0.95, "bottom": 0.05}

# <ToOverviewAndBudget>:
#     anchor_x: "right"
#     anchor_y: "bottom"
#     MDFloatingActionButton:
#         id: mode_expense
#         icon: "account-eye"
#         on_release: root.parent.load_widget("budget")
#         pos_hint: {'x': 0.9, 'y': 0.05}

# <ToExpense>:
#     anchor_x: "right"
#     anchor_y: "bottom"
#     MDFloatingActionButton:
#         id: mode_budget
#         icon: "notebook-edit-outline"
#         on_release: root.parent.load_widget("expense")
#         pos_hint: {'x': 0.9, 'y': 0.05}
        
<DatePicker>:
    anchor_x: "center" 
    anchor_y: "top"
    MDRaisedButton:
        id: picked_date
        size_hint_x: 0.6
        font_size: 30
        md_bg_color: (0.787, 0.957, 0.847)
        on_release: self.parent.show_date_picker()
        text: "Today"   

<DateRangePicker>:
    anchor_x: "center" 
    anchor_y: "top"
    MDRaisedButton:
        id: picked_date_range
        size_hint_x: 0.6
        font_size: 30
        md_bg_color: (0.787, 0.957, 0.847)
        on_release: self.parent.show_date_picker()
        text: "This Month"   

<MDFoodButton>:
    icon_size: "26sp"
    icon: "food"
    md_bg_color: rgba("#fbc6c6")
<MDTransportButton>:
    icon_size: "26sp"
    icon: "train-car"
    md_bg_color: rgba("#fbe8c6")
<MDHousingButton>:
    icon_size: "26sp"
    icon: "washing-machine"
    md_bg_color: rgba("#edffc2")
<MDEntertainmentButton>:
    icon_size: "26sp"
    icon: "teddy-bear"
    md_bg_color: rgba("#c2e6ff")
<MDOtherButton>:
    icon_size: "26sp"
    icon: "shopping"
    md_bg_color: rgba("#d7c2ff")
    '''


class MDFoodButton(MDIconButton):
    pass


class MDTransportButton(MDIconButton):
    pass


class MDHousingButton(MDIconButton):
    pass


class MDEntertainmentButton(MDIconButton):
    pass


class MDOtherButton(MDIconButton):
    pass


class ToExpense(MDAnchorLayout):
    pass


class ToOverviewAndBudget(MDAnchorLayout):
    pass


class SwitchMode(MDFloatingActionButtonSpeedDial):
    data = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {
            "Budget and Overview": [
                "account-eye",
                "on_release", lambda x: self.parent.load_widget("budget")
            ],
            'Edit Expense': [
                "notebook-edit-outline",
                "on_release", lambda x: self.parent.load_widget("expense")
            ],
        }