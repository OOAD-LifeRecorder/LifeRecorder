from datetime import datetime, date

from libs.kivymd_package import *
from libs.Database.ToDoDatabase import ToDoDatabase

from Components.ToDoList.DialogContent import DialogContent
from Components.ToDoList.TaskItem import TaskItem

class ToDoListScreen(MDScreen):
    def __init__(self, to_do_list_module, **kwargs):
        super(ToDoListScreen, self).__init__(**kwargs)
        self.name = "To-Do List"
        self.to_do_list_module = to_do_list_module
        self.add_widget(self.to_do_list_module)

class ToDoListModule(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = ToDoDatabase()
        self.setup_task_dialog()
        self.add_category_panel()
        self.add_to_do_list()
        self.add_add_button()

    def add_category_panel(self):
        self.category_list = MDList()
        self.category_state = 0
        self.selected_category = OneLineAvatarIconListItem(
            IconLeftWidget(
                icon="circle-small",
            ),
            IconRightWidget(
                icon="chevron-left",
                id="chevron"
            ),
            text="All",
            bg_color=(91/256,191/256,205/256,255/256),
            on_release=self.category_panel_on_press
        )
        self.category_list.add_widget(self.selected_category)
        self.add_widget(self.category_list)

    def add_to_do_list(self):
        self.to_do_list = MDBoxLayout(orientation="vertical")
        self.to_do_list_completed = MDList()
        self.to_do_list_uncomplete = MDList()

        self.add_uncomplete_and_completed_list_item()

        scroll_view_uncomplete = MDScrollView(do_scroll=(False, True))
        scroll_view_uncomplete.add_widget(self.to_do_list_uncomplete)
        
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Date",
                "on_release": lambda x=f"Date": self.set_item(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": f"Priority",
                "on_release": lambda x=f"Priority": self.set_item(x),
            },
        ]
        self.drop_item = MDRectangleFlatButton(
            pos_hint={'center_x': .5, 'center_y': .5},
            text='Date',
            on_release=self.open_menu
        )

        self.drop_menu = MDDropdownMenu(
            caller=self.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        
        self.to_do_list.add_widget(
            MDBoxLayout(
                MDLabel(
                    text="Undone", 
                    padding=[20, 10], 
                    bold=True
                ),
                self.drop_item,
                orientation="horizontal",
                size_hint_y=.1,
            )
        )
        self.to_do_list.add_widget(scroll_view_uncomplete)

        scroll_view_completed = MDScrollView(do_scroll=(False, True))
        scroll_view_completed.add_widget(self.to_do_list_completed)
        self.to_do_list.add_widget(
            MDLabel(text="Done", size_hint_y=0.15, padding=[20, 10], bold=True))
        self.to_do_list.add_widget(scroll_view_completed)

        self.add_widget(self.to_do_list)

    def add_uncomplete_and_completed_list_item(self, category="All"):
        completed_tasks, uncomplete_tasks = self.db.get_tasks(category)

        if uncomplete_tasks != []:
            for task in uncomplete_tasks:
                add_task = TaskItem(
                    pk=task[0],
                    text=task[1], 
                    secondary_text=task[2],
                    tertiary_text=task[5], 
                    priority=task[4]
                )
                add_task.check.bind(on_release=self.mark_task)
                add_task.delete_button.bind(on_release=self.delete_task)
                self.to_do_list_uncomplete.add_widget(add_task)

        if completed_tasks != []:
            for task in completed_tasks:
                add_task = TaskItem(
                    pk=task[0],
                    text=task[1], 
                    secondary_text=task[2], 
                    priority=task[4]
                )
                add_task.check.active = True
                add_task.check.bind(on_release=self.mark_task)
                add_task.delete_button.bind(on_release=self.delete_task)
                self.to_do_list_completed.add_widget(add_task)

    def open_menu(self, _):
        self.drop_menu.open()

    def set_item(self, type) -> None:
        self.to_do_list_uncomplete.clear_widgets()
        uncomplete_tasks = self.db.get_ordered_uncomplete_tasks(
            category=self.selected_category.text ,type=type)
        if uncomplete_tasks != []:
            for task in uncomplete_tasks:
                add_task = TaskItem(
                    pk=task[0],
                    text=task[1], 
                    secondary_text=task[2],
                    tertiary_text=task[5],  
                    priority=task[4]
                )
                add_task.check.bind(on_release=self.mark_task)
                add_task.delete_button.bind(on_release=self.delete_task)
                self.to_do_list_uncomplete.add_widget(add_task)
        self.drop_menu.dismiss()
        self.drop_item.text=type
        

    def add_add_button(self):
        self.add_button = MDFillRoundFlatButton(
            text="Add New Task",
            size_hint=(.95, .1),
            pos_hint={'center_y': .5, 'center_x': .5}
        )
        self.add_button.bind(on_release=self.show_task_dialog)
        self.add_widget(self.add_button)

    def date_on_active(self, _):
        print("date")

    def priority_on_active(self, _):
        print("priority")

    def mark_task(self, check):
        if check.active == True:
            self.to_do_list_uncomplete.remove_widget(check.parent.parent)
            check.parent.parent.text = '[s]'+check.parent.parent.text+'[/s]'
            self.db.mark_task_as_complete(check.parent.parent.pk)
            self.to_do_list_completed.add_widget(check.parent.parent)
        else:
            self.to_do_list_completed.remove_widget(check.parent.parent)
            check.parent.parent.text = str(self.db.mark_task_as_incomplete(check.parent.parent.pk))
            self.to_do_list_uncomplete.add_widget(check.parent.parent)

    def delete_task(self, instance):
        task_list = instance.parent.parent.parent.parent
        task = instance.parent.parent.parent
        task_list.remove_widget(task)
        self.db.delete_task(task.pk)

    def setup_task_dialog(self):
        self.task_dialog = MDDialog(
            title="Create Task",
            type="custom",
            content_cls=DialogContent(
                orientation="vertical",
                spacing="10dp",
                size_hint=(1, None),
                height="300dp"
            ),
        )
        self.task_dialog.content_cls.save_button.bind(
            on_press=self.add_task)
        self.task_dialog.content_cls.cancel_button.bind(
            on_release=self.close_dialog)

    def show_task_dialog(self, _):
        self.task_dialog.open()

    def add_task(self, _):
        created_task = self.db.create_task(
            self.task_dialog.content_cls.task_title.text,
            int(self.task_dialog.content_cls.prior_button.text), 
            self.task_dialog.content_cls.date_text.text,
            self.task_dialog.content_cls.category_text.text
        )
        print(created_task)
        self.to_do_list_uncomplete.add_widget(
            TaskItem(
                pk=created_task[0], 
                text='[b]'+created_task[1]+'[/b]', 
                secondary_text=created_task[2],
                tertiary_text=created_task[5], 
                priority=created_task[4]
            )
        )
        self.close_dialog()

    def close_dialog(self, *args):
        self.task_dialog.dismiss()

    def category_panel_on_press(self, instance):
        if self.category_state == 0:
            category_list = self.db.get_category_list()
            for category in category_list:
                text = category[0] if category[0] != "" else "None"
                if self.selected_category.text == text:
                    text = "All"
                self.category_list.add_widget(
                    OneLineAvatarIconListItem(
                        IconLeftWidget(
                            icon="circle-small",
                        ),
                        text=text,
                        bg_color=(232/256,246/256,248/256,255/256),
                        divider_color=(91/256,191/256,205/256,255/256),
                        on_release=self.category_on_press
                    )
                )
            self.category_state = 1
            self.selected_category.ids.chevron.icon = "chevron-down"
        else:
            self.close_panel(instance)

    def category_on_press(self, instance):
        text_selected = instance.text
        instance.text = self.selected_category.text
        self.selected_category.text = text_selected
        self.to_do_list_completed.clear_widgets()
        self.to_do_list_uncomplete.clear_widgets()
        self.add_uncomplete_and_completed_list_item(category=text_selected)
        self.drop_item.text = "Date"
        self.close_panel(self.selected_category)

    def close_panel(self, instance):
        self.category_list.clear_widgets()
        self.category_state = 0
        self.selected_category.ids.chevron.icon = "chevron-left"
        self.category_list.add_widget(instance)

class RightItems(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True