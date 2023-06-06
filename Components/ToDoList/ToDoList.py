from libs.kivymd_package import *

from Components.ToDoList.TaskItem import TaskItem
from libs.Database.ToDoDatabase import ToDoDatabase

class ToDoList(MDList):
    def __init__(self, tasks_list, **kwargs):
        super().__init__(**kwargs)
        self.tasks_list = tasks_list
        self.db = ToDoDatabase()

        self.add_task_list()

    def add_task_list(self):
        print(self.tasks_list)
        for task in self.tasks_list:
            add_task = TaskItem(
                pk=task[0],
                text=task[1], 
                secondary_text=task[2],
                tertiary_text=task[5],
                priority=task[4],
                size_hint_x=.8,
                pos_hint={"center_x": .5}
            )
            if task[3]:
                add_task.text = '[s]'+task[1]+'[/s]'
                add_task.check.active = True
            add_task.check.bind(on_release=self.mark_task)
            add_task.delete_button.bind(on_release=self.delete_task)
            self.add_widget(add_task)

    def mark_task(self, check):
        task = check.parent.parent
        self.remove_widget(task)
        if check.active == True:
            task.text = '[s]'+task.text+'[/s]'
            self.db.mark_task_as_complete(task.pk)
        else:
            task.text = str(self.db.mark_task_as_incomplete(task.pk))
        return task

    def delete_task(self, instance):
        task = instance.parent.parent.parent
        self.remove_widget(task)
        self.db.delete_task(task.pk)