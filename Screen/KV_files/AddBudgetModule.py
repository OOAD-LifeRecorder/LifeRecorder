from Screen.KV_files.ExpenseTrackerScreenKV import *
from kivymd.uix.list import TwoLineAvatarIconListItem


AddBudgetModuleKV = '''
<AddBudgetModule>:
    size_hint: ( 0.9, 0.83 )
    row_default_height: self.height/13
    pos_hint: {'center_x': .5, 'y':.05}
    spacing: "5dp"
    cols: 1

    budget_list_widget: budget_list_widget.__self__
    budget_amount: budget_amount.__self__

    # ButtonExpenseType
    MDGridLayout:
        rows: 1
        MDAnchorLayout:
            anchor_x: "right"
            size_hint_x: 0.2
            MDAllButton:
                id: all
                on_release: root.set_budget_type("all")
        MDAnchorLayout:
            anchor_x: "center"
            size_hint_x: 0.16
            MDFoodButton:
                id: food
                on_release: root.set_budget_type("food")
        MDAnchorLayout:
            anchor_x: "center"
            size_hint_x: 0.125
            MDTransportButton:
                id: transport
                on_release: root.set_budget_type("transport")
        MDAnchorLayout:
            anchor_x: "center"
            size_hint_x: 0.125
            MDHousingButton:
                id: housing
                on_release: root.set_budget_type("housing")
        MDAnchorLayout:
            anchor_x: "center"
            size_hint_x: 0.16
            MDEntertainmentButton:
                id: entertainment
                on_release: root.set_budget_type("entertainment")
        MDAnchorLayout:
            anchor_x: "left"
            size_hint_x: 0.2
            MDOtherButton:
                id: other
                on_release: root.set_budget_type("other")

    # Enter Budget
    MDGridLayout:
        rows: 1
        MDAnchorLayout:
            size_hint_x : 0.175
            anchor_x: "right"
            IconLeftWidget:
                icon: "currency-usd"
                icon_size: "30sp"
        MDAnchorLayout:
            anchor_x: "left"
            size_hint_x: 0.7
            MDTextField:
                id: budget_amount
                size_hint_x: 0.8
                hint_text: "Enter your budget for this month..."
                input_filter : 'int'
                multiline: False
                font_size: 16

    # AddBudgetButton:
    MDGridLayout:
        rows: 1
        MDAnchorLayout:
            anchor_x: "right"
            MDRectangleFlatButton:
                id: clear
                font_size: 20
                size_hint_x: 0.6
                text: "Clear"
                on_press: root.reset_input()
                theme_text_color: "Custom"
                text_color: "white"
                line_color: "red"
                md_bg_color: rgba("#ff6464")

        ##### padding #####
        MDAnchorLayout:
            size_hint_x: 0.2
            anchor_x: "center"
        ##### padding #####

        MDAnchorLayout:
            anchor_x: "left"
            MDRectangleFlatButton:
                id: add 
                font_size: 20
                size_hint_x: 0.6
                text: "Save"
                on_press: root.set_budget_amount()
                theme_text_color: "Custom"
                text_color: "white"
                line_color: "green"
                md_bg_color: rgba("#a4ffa4") 

    MDGridLayout:
        rows: 1
        size_hint: ( 0.6, 1)
        pos_hint: {'center_x': .5 }
        canvas:
            Color:
                rgba: rgba("#d3ffee")
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [(15, 15), (15, 15), (15, 15), (15, 15)]
        MDLabel:
            halign:"center"
            id:date_range
            font_style: "Button"

    # ShowExpenseWithSurplus
    MDGridLayout:
        cols: 1
        #md_bg_color: rgba("#f8efff")
        size_hint: ( 0.6, 8)
        pos_hint: {'center_x': .5, 'y':.175}

        MDAnchorLayout:
            anchor_x : "center"
            canvas:
                Color:
                    rgba: rgba("#DDDDDD")
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [(15, 15), (15, 15), (15, 15), (15, 15)]
            MDScrollView:
                # id: scrollable_container
                do_scroll_y: True
                bar_width: 3
                minimum_height: root.setter('height')
                minimum_width: self.parent.width
                MDList:
                    id: budget_list_widget

    ########################### Budget #############################
    MDBoxLayout:
        orientation: "vertical"
        size_hint: ( 0.7, 0.14 )
        pos_hint: {'center_x': .5, 'y':.01}

        MDGridLayout:
            cols: 4
            spacing: "5dp"
        
            MDLabel:
                text: "Total Expense: "
                font_style: "Caption"
            MDLabel:
                id: total_expense
                text_color: "red"
                font_style: "Caption"

            MDLabel:
                text: "Budget/day: "
                font_style: "Caption"
            MDLabel:
                id: expense_per_day
                font_style: "Caption"
                text_color: "green"
            

        MDGridLayout:
            rows: 1
            canvas:
                Color:
                    rgba: rgba("#d3ffee")
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [(15, 15), (15, 15), (15, 15), (15, 15)]
            MDLabel:
                text: "Budget surplus (month): "
                font_style: "Subtitle2"
                # text_color:
            MDLabel:
                id: surplus_month
                font_style: "Subtitle2"
                text_color: "green"

    ########################### Budget #############################
<MDAllButton>:
    icon_size: "20sp"
    icon: "all-inclusive"
    md_bg_color: rgba("#fcefff")


<ListBudgetItemWithIcon>:
    id: the_list_item
    markup: True
    # on_size: 
    #     self.ids._right_container.x = container.width
    #     self.ids._right_container.width = container.width

    IconLeftWidgetWithoutTouch:
        id: the_item_icon    
'''


class MDAllButton(MDIconButton):
    pass


class ListBudgetItemWithIcon(TwoLineAvatarIconListItem):
    pass
