from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.properties import ObjectProperty

from libs.kivymd_package import *
from Screen.CalendarScreen import CalendarScreen
from Screen.NotesScreen import NotesScreen
from Screen.ToDoListScreen import ToDoListScreen
from Screen.ExpenseTrackerScreen import ExpenseTrackerScreen


KV = '''
<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)

    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color

<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    MDLabel:
        text: "Life Recorder"
        font_style: "Button"
        adaptive_height: True

    ScrollView:
        DrawerList:
            ItemDrawer:
                text: "Calendar"
                icon: "calendar"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "Calendar"

            ItemDrawer:
                text: "Notes"
                icon: "note"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "Notes"

            ItemDrawer:
                text: "To-Do List"
                icon: "format-list-checkbox"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "To-Do List"

            ItemDrawer:
                text: "Expense Tracker"
                icon: "currency-usd"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "Expense Tracker"



MDBoxLayout:
    orientation: "vertical"
    MDTopAppBar:
        id: toolbar
        title: "Life Recorder"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
    
    MDNavigationLayout:
        x: toolbar.height

        ScreenManager:
            id: screen_manager

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                id: content_drawer

                screen_manager: screen_manager
                nav_drawer: nav_drawer

'''

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))

class DrawerList(MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.hue = '100'
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)
    
    def on_start(self):
        screens = [
            CalendarScreen(),
            NotesScreen(),
            ToDoListScreen(),
            ExpenseTrackerScreen()
        ]
        for screen in screens:
            self.root.ids.screen_manager.add_widget(
                screen
            )


MainApp().run()