from kivy.utils import rgba

from libs.kivymd_package import *
from libs.Database.ToDoDatabase import ToDoDatabase
from datetime import datetime, timedelta

from Components.Calendar.WeekTab import WeekTab
from Components.ToDoList.ToDoList import ToDoList

class CalendarScreen(MDScreen):
    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)
        self.name = "Calendar"
        self.add_widget(CalendarModule(orientation="vertical"))

class CalendarModule(MDBoxLayout):
    def __init__(self, **kwargs):
        super(CalendarModule, self).__init__(**kwargs)
        self.date_shown = datetime.now()
        self.__todo_db = ToDoDatabase()
        self.__add_calendar_bar()
        self.__add_calendar_content()

    def today_on_press(self, _):
        self.change_date(datetime.now())

    def on_week_day_press(self, instance, ref):
        if instance.parent == self._current_tab:
            return
        instance.parent.change_active_state()
        self._current_tab.change_active_state()

        self._current_tab = instance.parent
        self.change_date(datetime.strptime(ref, '%Y%m%d'))

    def show_date_picker(self, _):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.change_date(value)

    def change_date(self, date):
        print("change_date")
        self.date_shown = date
        self.week_days_carousel.clear_widgets()
        self.__add_week_days_layout(self.date_shown)

        self.calendar_content.remove_widget(self.day_list)
        self.day_list = self.get_layout()
        self.calendar_content.add_widget(self.day_list)

        self.month_button.text = self.date_shown.strftime("%Y %B")
    
    def __add_calendar_bar(self):
        self.__add_month_bar_layout()
        self.add_widget(self.__get_week_bar())
        self.__add_week_days_carousel()

    def __add_calendar_content(self):
        self.calendar_content = MDScrollView(do_scroll=(False, True))
        self.day_list = self.get_layout()
        self.calendar_content.add_widget(self.day_list)
        self.add_widget(self.calendar_content)

    def __add_month_bar_layout(self):
        month_bar_layout = MDBoxLayout(
            orientation="horizontal", size_hint_y=.1)
        self.month_button = MDRectangleFlatButton(
            text=self.date_shown.strftime("%Y %B"),
            size_hint=(.8, None),
        )
        self.month_button.bind(on_release=self.show_date_picker)
        self.today_button = MDRectangleFlatButton(
            text="Today")
        self.today_button.bind(on_release=self.today_on_press)
        month_bar_layout.add_widget(self.month_button)
        month_bar_layout.add_widget(self.today_button)
        self.add_widget(month_bar_layout)

    def __get_week_bar(self):
        week_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=0.08
        )
        week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for week_day in week:
            week_bar.add_widget(MDLabel(
                text=f'[color=009688]{week_day}[/color]', 
                halign="center",
                markup = True
            ))
        return week_bar

    def __add_week_days_carousel(self):
        # 取得當月天數
        self.week_days_carousel = MDCarousel(
            direction='right', 
            size_hint_y=.08,
            loop=True
        )
        
        self.week_days_carousel.bind(on_slide_complete=self.carousel_slide_complete)
        self.__add_week_days_layout(self.date_shown)
        self.add_widget(self.week_days_carousel)

    def carousel_slide_complete(self, carousel, left, now, right):
        carousel.remove_widget(left)
        carousel.remove_widget(right)
        index = len(now.children) - 1
        now_first_date = datetime.strptime(now.children[index].ref, '%Y%m%d')
        carousel.add_widget(self.__get_week_days_layout(now_first_date + timedelta(days=7)))
        carousel.add_widget(self.__get_week_days_layout(now_first_date - timedelta(days=7)))
        self.month_button.text = now_first_date.strftime("%Y %B")

    def __add_week_days_layout(self, date):
        pre_slide_date = date - timedelta(days=7)
        next_slide_date = date + timedelta(days=7)
        self.week_days_carousel.add_widget(
            self.__get_week_days_layout(date))
        self.week_days_carousel.add_widget(
            self.__get_week_days_layout(next_slide_date))
        self.week_days_carousel.add_widget(
            self.__get_week_days_layout(pre_slide_date))
    
    def __get_week_days_layout(self, date):
        first_date = date - timedelta(days=self.date_shown.weekday())
        bar_list = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=.8
        )
        for i in range(0, 7):
            now_date = first_date + timedelta(days=i)
            date_shown = now_date.strftime('%d')
            ref = now_date.strftime('%Y%m%d')
            if now_date.date() == self.date_shown.date():
                tab = WeekTab(ref=ref, text=date_shown, active=True)
                self._current_tab = tab
            else:
                tab = WeekTab(ref=ref, text=date_shown)

            tab.label.bind(on_ref_press=self.on_week_day_press)
            bar_list.add_widget(tab)
        return bar_list

    def get_layout(self):
        layout = MDList()

        # 從第一天開始填入日期
        for i in range(0, 7):
            now_date = self.date_shown + timedelta(days=i)
            text_shown = now_date.strftime("%m/%d %a")
            _, to_do_list_uncomplete = self.__todo_db.get_tasks_by_date(now_date)
            
            day_card =  OneLineAvatarIconListItem(
                IconLeftWidget(icon="calendar"),
                text=text_shown
            )
            layout.add_widget(day_card)
            layout.add_widget(
                ToDoList(
                    to_do_list_uncomplete,
                    size_hint_x=.8,
                    pos_hint={"center_x": .5}
                )
            )

        return layout
    
