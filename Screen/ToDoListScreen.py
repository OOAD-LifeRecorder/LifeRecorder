from datetime import datetime, date

from libs.kivymd_package import *
from libs.Database.ToDoDatabase import ToDoDatabase

from Components.ToDoList.DialogContent import DialogContent
from Components.ToDoList.TaskItem import TaskItem

class ToDoListScreen(MDScreen):
    def __init__(self, **kwargs):
        super(ToDoListScreen, self).__init__(**kwargs)
        self.name = "To-Do List"
        self.to_do_list_module = ToDoListModule(orientation="vertical")
        self.add_widget(self.to_do_list_module)

class ToDoListModule(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = ToDoDatabase()
        self.task_dialog = None
        self.add_to_do_list()
        self.add_add_button()

    def add_to_do_list(self):
        self.to_do_list = MDBoxLayout(orientation="vertical")
        self.to_do_list_completed = MDList()
        self.to_do_list_uncomplete = MDList()

        completed_tasks, uncomplete_tasks = self.db.get_tasks()

        if uncomplete_tasks != []:
            for task in uncomplete_tasks:
                add_task = TaskItem(pk=task[0],text=task[1], secondary_text=task[2])
                add_task.check.bind(on_release=self.mark_task)
                add_task.delete_button.bind(on_release=self.delete_task)
                self.to_do_list_uncomplete.add_widget(add_task)

        if completed_tasks != []:
            for task in completed_tasks:
                add_task = TaskItem(pk=task[0],text='[s]'+task[1]+'[/s]', secondary_text=task[2])
                add_task.check.active = True
                add_task.check.bind(on_release=self.mark_task)
                add_task.delete_button.bind(on_release=self.delete_task)
                self.to_do_list_completed.add_widget(add_task)

        scroll_view_uncomplete = MDScrollView(do_scroll=(False, True))
        scroll_view_uncomplete.add_widget(self.to_do_list_uncomplete)
        self.to_do_list.add_widget(
            MDLabel(text="Undone", size_hint_y=0.15, padding=[20, 10], bold=True))
        self.to_do_list.add_widget(scroll_view_uncomplete)

        scroll_view_completed = MDScrollView(do_scroll=(False, True))
        scroll_view_completed.add_widget(self.to_do_list_completed)
        self.to_do_list.add_widget(
            MDLabel(text="Done", size_hint_y=0.15, padding=[20, 10], bold=True))
        self.to_do_list.add_widget(scroll_view_completed)

        self.add_widget(self.to_do_list)

    def add_add_button(self):
        self.add_button = MDFillRoundFlatButton(
            text="Add New Task",
            size_hint=(.95, .1),
            pos_hint={'center_y': .5, 'center_x': .5}
        )
        self.add_button.bind(on_release=self.show_task_dialog)
        self.add_widget(self.add_button)

    def mark_task(self, check):
        print(check.parent.parent)
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

    def show_task_dialog(self, _):
        if not self.task_dialog:
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
                on_release=self.add_task)
            self.task_dialog.content_cls.cancel_button.bind(
                on_release=self.close_dialog)

        self.task_dialog.open()

    def add_task(self, _):
        created_task = self.db.create_task(
            self.task_dialog.content_cls.task_title.text, 
            self.task_dialog.content_cls.date_text.text
        )

        self.to_do_list_uncomplete.add_widget(
            TaskItem(
                pk=created_task[0], 
                text='[b]'+created_task[1]+'[/b]', 
                secondary_text=created_task[2]
            )
        )
        self.close_dialog()

    def close_dialog(self, *args):
        self.task_dialog.dismiss()