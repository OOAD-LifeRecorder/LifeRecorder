from datetime import date

from libs.kivymd_package import *


class DialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_selected = date.today()
        self.add_title_input_layout()
        self.add_date_input_layout()
        self.add_button_layout()

    def add_date_input_layout(self):
        date_input_layout = MDGridLayout(rows=1)

        self.date_text = MDTextField(
            text=self.date_selected.strftime('%Y/%m/%d'),
            validator="date",
            date_format="yyyy/mm/dd",
            required=True
        )
        date_picker = MDIconButton(
            icon='calendar',
            on_release=self.show_date_picker,
            padding='20dp'
        )
            
        date_input_layout.add_widget(self.date_text)
        date_input_layout.add_widget(date_picker)
        self.add_widget(date_input_layout)

    def add_title_input_layout(self):
        self.task_title = MDTextField(
            hint_text="Title",
            max_text_length=30,
            required=True
        )
        self.add_widget(self.task_title)

    def add_button_layout(self):
        button_layout = MDBoxLayout(orientation="horizontal")

        self.save_button = MDRaisedButton(text="SAVE")
        self.cancel_button = MDFlatButton(text="CANCEL")

        button_layout.add_widget(self.save_button)
        button_layout.add_widget(self.cancel_button)
        self.add_widget(button_layout)

    def show_date_picker(self, _):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.selected_date = value
        self.date_text.text = value.strftime('%Y/%m/%d')