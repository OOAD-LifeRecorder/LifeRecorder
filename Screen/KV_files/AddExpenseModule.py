from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.list import TwoLineAvatarIconListItem
from libs.kivymd_package import *

AddExpenseModuleKV = '''
#:import rgba kivy.utils.get_color_from_hex
<AddExpenseModule>: 
    # md_bg_color: rgba("#f5efff")
    size_hint: ( 0.9, 0.83 )
    row_default_height: self.height/12
    pos_hint: {'center_x': .5, 'y':.05}
    spacing: "3dp"
    cols: 1

    expense_list_widget: expense_list_widget.__self__

    # ButtonExpenseType
    MDGridLayout:
        rows: 1
        MDAnchorLayout:
            anchor_x: "right"
            size_hint_x: 0.25
            MDFoodButton:
                id: food
                on_release: root.set_expense_type("food")
        MDAnchorLayout:
            anchor_x: "right"
            size_hint_x: 0.15
            MDTransportButton:
                id: transport
                on_release: root.set_expense_type("transport")
        MDAnchorLayout:
            anchor_x: "center"
            size_hint_x: 0.2
            MDHousingButton:
                id: housing
                on_release: root.set_expense_type("housing")
        MDAnchorLayout:
            anchor_x: "left"
            size_hint_x: 0.15
            MDEntertainmentButton:
                id: entertainment
                on_release: root.set_expense_type("entertainment")
        MDAnchorLayout:
            anchor_x: "left"
            size_hint_x: 0.25
            MDOtherButton:
                id: other
                on_release: root.set_expense_type("other")

    # Name Expense
    MDGridLayout:
        rows: 1
        MDAnchorLayout:
            size_hint_x : 0.175
            anchor_x: "right"
            IconLeftWidget:
                icon: "cart"
                icon_size: "30sp"
        MDAnchorLayout:
            anchor_x: "left"
            size_hint_x: 0.7
            MDTextField:
                id: expense_name
                size_hint_x: 0.8
                font_size: 16
                hint_text: "Name your expense..."
                on_text_validate: root.set_expense_name()
                multiline: False
    
    # Enter Expense
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
                id: expense_amount
                size_hint_x: 0.8
                font_size: 16
                hint_text: "How much did you spend?"
                on_text_validate: root.set_expense_amount()
                input_filter : 'int'
                multiline: False
    
    # AddExpenseButton:
    MDGridLayout:
        rows: 1
        MDAnchorLayout:
            anchor_x: "right"
            MDRectangleFlatButton:
                id: clear
                font_size: 20
                size_hint_x: 0.6
                text: "Clear"
                on_press: root.clear_input()
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
                text: "Add"
                on_press: root.save_expense()
                theme_text_color: "Custom"
                text_color: "white"
                line_color: "green"
                md_bg_color: rgba("#a4ffa4")       

    #ShowExpenseModule:
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
                #ExpenseList:
                    id: expense_list_widget

    ########################### Budget #############################
    MDBoxLayout:
        orientation: "vertical"
        size_hint: ( 0.7, 0.14 )
        pos_hint: {'center_x': .5, 'y':.01}

        MDGridLayout:
            rows: 1
            spacing: "5dp"
            canvas:
                Color:
                    rgba: rgba("#d3ffee")
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [(15, 15), (15, 15), (15, 15), (15, 15)]
            
            MDLabel:
                text: "Total Expense: "
                font_style: "Subtitle2"
            MDLabel:
                id: total_expense
                text_color: "red"
                font_style: "Subtitle2"
            
        MDGridLayout:
            rows: 1
            MDLabel:
                text: "Budget surplus (month): "
                font_style: "Caption"
                # text_color:
            MDLabel:
                id: surplus_month
                font_style: "Caption"
                text_color: "green"
            MDLabel:
                text: "Budget surplus (today): "
                font_style: "Caption"
                # text_color:
            MDLabel:
                id: surplus_day
                font_style: "Caption"
                text_color: "green"

    ########################### Budget #############################

<ListExpenseItemWithIcon>:
    id: the_list_item
    markup: True
    on_size: 
        self.ids._right_container.x = container.width
        self.ids._right_container.width = container.width
    on_release:
        self.update_current_expense(the_list_item)

    IconLeftWidgetWithoutTouch:
        id: the_item_icon

    RightButtons:
        id: container
        adaptive_width: True

        MDIconButton:
            id: the_item_edit
            icon: 'square-edit-outline'
            on_release:
                root.update_current_expense(the_list_item)
            
        MDIconButton:
            id: the_item_delete
            icon: 'trash-can-outline'
            on_release:
                root.delete_item(the_list_item)

'''


class RightButtons(IRightBodyTouch, MDBoxLayout):
    pass


class AddExpenseInput(MDGridLayout):
    pass


class ListExpenseItemWithIcon(TwoLineAvatarIconListItem):
    # pass
    def __init__(self, current_module=None, **kwargs):
        super().__init__(**kwargs)
        self.current_module = current_module

    def delete_item(self, the_list_item):
        widget_index = self.parent.children.index(the_list_item)
        expense_index = len(self.parent.children)-widget_index-1
        self.current_module.delete_list_item(expense_index)
        self.parent.remove_widget(the_list_item)

    def update_current_expense(self, the_list_item):
        widget_index = self.parent.children.index(the_list_item)
        for item in self.parent.children:
            item.bg_color = "#DDDDDD"

        self.bg_color = "#afefdd"
        self.current_module.update_value(widget_index, self)

    # def edit_date(self, the_list_item):
    #     self.current_screen.show_date_picker()
