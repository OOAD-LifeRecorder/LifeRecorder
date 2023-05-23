
from libs.kivymd_package import *
from libs.TimeModule import get_month_information, get_weekday_str

class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class CalendarScreen(MDScreen):
    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)
        self.name = "Calendar"
        self.add_widget(CalendarModule(orientation="vertical"))

class CalendarModule(MDBoxLayout):
    def __init__(self, **kwargs):
        super(CalendarModule, self).__init__(**kwargs)
        self.get_calendar_bar()
        self.get_calendar_content()

    def get_calendar_bar(self):
        month_information = get_month_information()

        self.add_widget(MDTopAppBar(
            title=month_information['today'].strftime("%Y %B")))
        self.add_widget(self.get_bar_layout(month_information))


    def get_calendar_content(self):
        calendar_content = MDScrollView(
            do_scroll_x=False, do_scroll_y=True)
        month_information = get_month_information()
        calendar_content.add_widget(self.get_layout(month_information))
        self.add_widget(calendar_content)

    def get_bar_layout(self, month_information: dict):
        # 取得當月天數
        month = month_information['today'].month
        month_days = month_information['last_day'].day
        week_day = month_information['first_day'].weekday()

        bar_list = MDTabs(id="tabs")
        bar_list.bind(on_tab_switch=bar_list.on_tab_switch)
        for i in range(1, month_days + 1):
            bar_list.add_widget(
                Tab(
                    title=f"{month}/{i}"
                )
            )
        return bar_list

    def get_layout(self, month_information: dict):
        # 取得當月天數
        month = month_information['today'].month
        month_days = month_information['last_day'].day
        week_day = month_information['first_day'].weekday()

        # 建立一個網格布局，每個格子是一列
        layout = MDGridLayout(
            cols=1,  
            spacing="8db",
            padding="8db",
            adaptive_height=True
        )
        layout.bind(minimum_height=layout.setter('height'))

        # 從第一天開始填入日期
        for i in range(1, month_days + 1):
            text_shown = f"{month}/{i} ({get_weekday_str(week_day%7)})"
            week_day += 1
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