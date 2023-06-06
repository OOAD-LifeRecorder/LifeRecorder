from libs.kivymd_package import *
from libs.Database.ToDoDatabase import ToDoDatabase
from libs.Database.EventDatabase import EventDatabase
from datetime import datetime, timedelta

from Components.Calendar.WeekTab import WeekTab
from Components.Calendar.EventCard import EventCard
from Components.Calendar.DialogContent import DialogContent
from Components.ToDoList.ToDoList import ToDoList

class CalendarScreen(MDScreen):
    def __init__(self, to_do_list_module, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)
        self.name = "Calendar"
        self.to_do_list_module = to_do_list_module
        self.calendar_module = CalendarModule(
            self.to_do_list_module,
            orientation="vertical"
        )
        self.to_do_list_module.task_dialog.content_cls.save_button.bind(
            on_release=self.reload_task)
        self.add_widget(self.calendar_module)
        self.add_widget(self.add_button())

    def add_button(self):
        data = {
            "Event Tag": [
                "calendar-plus",
                "on_press", lambda x: print("Add Event"),
                "on_release", self.add_event_on_press
            ],
            "To-Do List": [
                "format-list-checkbox",
                "on_press", lambda x: print("Add Task"),
                "on_release", self.add_task_on_press
            ],
        }
        return MDFloatingActionButtonSpeedDial(
                    data=data,
                    hint_animation=False,
                    root_button_anim=True,
                )
    
    def add_task_on_press(self, *args):
        self.to_do_list_module.show_task_dialog(None)

    def add_event_on_press(self, *args):
        self.calendar_module.show_event_dialog(None)

    def reload_task(self, _):
        self.calendar_module.change_date(self.calendar_module.date_shown)
        

class CalendarModule(MDBoxLayout):
    def __init__(self, to_do_list_module, **kwargs):
        super(CalendarModule, self).__init__(**kwargs)
        self.date_shown = datetime.now()
        self.to_do_list_module = to_do_list_module
        self.event_dialog = None
        self.event_date_dict = {}
        self.__todo_db = ToDoDatabase()
        self.__event_db = EventDatabase()
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
            
            day_card =  OneLineAvatarIconListItem(
                IconLeftWidget(icon="calendar"),
                text=text_shown,
                bg_color=(220/256, 220/256, 220/256, 1)
            )
            layout.add_widget(day_card)
            date = now_date.strftime("%Y/%m/%d")
            events = self.__event_db.get_events_by_date(date)
            for event in events:
                event_card = EventCard(
                    event[0], event[1], event[2])
                layout.add_widget(event_card)
                event_card.delete_button.bind(on_release=self.delete_event)

                if date not in self.event_date_dict:
                    self.event_date_dict = []
                self.event_date_dict.append(event_card)
            
            _, to_do_list_uncomplete = self.__todo_db.get_tasks_by_date(now_date)
            layout.add_widget(
                ToDoList(
                    to_do_list_uncomplete,
                    size_hint_x=.8,
                    pos_hint={"center_x": .5}
                )
            )

        return layout
    
    def show_event_dialog(self, _):
        if not self.event_dialog:
            self.event_dialog = MDDialog(
                title="Create Event",
                type="custom",
                content_cls=DialogContent(
                    orientation="vertical",
                    spacing="10dp",
                    size_hint=(1, None),
                    height="300dp"
                ),
            )
            self.event_dialog.content_cls.save_button.bind(
                on_release=self.add_event)
            self.event_dialog.content_cls.cancel_button.bind(
                on_release=self.close_dialog)

        self.event_dialog.open()

    def add_event(self, _):
        self.__event_db.create_event(
            self.event_dialog.content_cls.event_title.text, 
            self.event_dialog.content_cls.date_text.text,
            self.event_dialog.content_cls.color_index
        )
        
        self.change_date(self.date_shown)
        self.close_dialog()

    def delete_event(self, instance):
        event_list = instance.parent.parent.parent
        event = instance.parent.parent
        event_list.remove_widget(event)
        self.__event_db.delete_event(event.pk)

    def close_dialog(self, *args):
        self.event_dialog.dismiss()
