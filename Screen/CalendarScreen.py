
from libs.kivymd_package import *
from datetime import datetime, timedelta

class CalendarScreen(MDScreen):
    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)
        self.name = "Calendar"
        self.add_widget(CalendarModule(orientation="vertical"))

class CalendarModule(MDBoxLayout):
    def __init__(self, **kwargs):
        super(CalendarModule, self).__init__(**kwargs)
        self.date_shown = datetime.now()
        self.get_calendar_bar()
        self.add_widget(self.get_calendar_content())

    def get_calendar_bar(self):
        self.add_widget(
            MDTopAppBar(
                title=self.date_shown.strftime("%Y %B"),
                type_height="small",
                elevation=1
            )
        )
        self.add_widget(self.get_week_bar())
        self.add_widget(self.get_bar_layout())

    def get_calendar_content(self):
        calendar_content = MDScrollView(do_scroll=(False, True))
        calendar_content.add_widget(self.get_layout())
        return calendar_content

    def get_week_bar(self):
        week_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=0.1
        )
        week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for week_day in week:
            week_bar.add_widget(MDLabel(
                text=f'[color=009688]{week_day}[/color]', 
                halign="center",
                markup = True
            ))
        return week_bar

    def get_bar_layout(self):
        # 取得當月天數
        first_date = self.date_shown - timedelta(days=self.date_shown.weekday())
        calendar_bar = MDCarousel(
            direction='right', 
            loop=True,
            size_hint_y=0.15
        )
        
        for k in range(4):
            bar_list = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None
            )
            for i in range(0, 7):
                now_date = first_date + timedelta(days=7*k+i)
                date_shown = now_date.strftime('%d')
                ref = now_date.strftime('%Y%m%d')

                if now_date == self.date_shown:
                    text_shown = f"[color=36454F]{date_shown}[/color]"
                else:
                    text_shown = f"[color=D3D3D3]{date_shown}[/color]"
                tab = MDLabel(
                    text=f"[ref={ref}]{text_shown}[/ref]",
                    halign="center",
                    markup=True,
                )
                if now_date == self.date_shown:
                    self._current_tab = tab
                tab.bind(on_ref_press=self.on_week_day_press)
                bar_list.add_widget(tab)
                
            calendar_bar.add_widget(bar_list)
        return calendar_bar
    
    def on_week_day_press(self, instance, ref):
        if instance == self._current_tab:
            return
        instance.text = instance.text.replace('D3D3D3', '36454F')
        self._current_tab.text = self._current_tab.text.replace('36454F', 'D3D3D3')
        self._current_tab = instance
        self.text_shown = datetime.strptime(ref, '%Y%m%d')

    def get_layout(self):
        # 建立一個網格布局，每個格子是一列
        layout = MDGridLayout(
            cols=1,  
            spacing="8db",
            padding="8db",
            adaptive_height=True
        )
        layout.bind(minimum_height=layout.setter('height'))

        # 從第一天開始填入日期
        for i in range(0, 10):
            now_date = self.date_shown + timedelta(days=i)
            text_shown = now_date.strftime("%m/%d %a")
            # 建立日期標籤和文字輸入框
            day_input = MDTextField(hint_text="Persistent helper text")
            day_card = MDExpansionPanel(
                icon="circle-small",
                content=day_input,
                panel_cls=MDExpansionPanelOneLine(
                    text=text_shown,
                )
            )

            # 將日期標籤和文字輸入框添加到網格布局中
            layout.add_widget(day_card)

        return layout