from kivy.lang import Builder
from libs.kivymd_package import *
from kivy.factory import Factory

from kivymd.uix.pickers import MDDatePicker
KV = '''
<DatePicker>:
    MDRaisedButton:
        size_hint: (1,0.3)
        text: root.get_current_date()
        on_release: root.show_date_picker()
        pos_hint: {'center_x': .5, 'y': .78}
        font_size: 42
        md_bg_color: 
    
<ButtonExpenseType>
    orientation: 'horizontal'
    MDIconButton:
        icon: "food"
        # callback: app.root.setExpenseEype("food")

MDGridLayout:
    anchor_y: 'top'
    cols: 1
    #adaptive_height: True
    # md_bg_color: app.theme_cls.primary_color
    DatePicker
    ButtonExpenseType
'''

class DatePicker(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__current_date = "Today"

    def get_current_date(self):
        return self.__current_date

    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        self.__current_date = value
        print(instance, value, date_range)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

class ButtonExpenseType(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {
            'food': 'Food',
            'train-car': 'Transport',
            'washing-machine': 'Housing',
            'teddy-bear': 'Entertainment',
            'shopping': 'Other'
        }


    def set_expense_type(self,instance):
        self.__init__setExpenseType()
        print("clicked!" + instance)

class Expense():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__type_ = ""
        self__date_ = ""
        self.__expense = 0
        self.__name = ""

    def setDate(self, val):
        self.__date = val

    def setExpense(self, val):
        self.__expense = val

    def setName(self, name):
        self.__name = name

    def setExpenseType( self, type):
        self.__type = type

class ExpenseTrackerScreen(MDScreen):
    def __init__(self, **kwargs):
        super(ExpenseTrackerScreen, self).__init__(**kwargs)
        self.name = "Expense Tracker"
        self.add_widget(
            MDLabel(
                text="Expense",
                halign="center"
            ),
        )

        self.current_expense = Expense()

        self.add_widget(Builder.load_string(KV))
        


