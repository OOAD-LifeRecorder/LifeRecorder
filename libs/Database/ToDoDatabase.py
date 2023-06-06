from libs.Database.Database import Database
from datetime import datetime

class ToDoDatabase(Database):
    def _create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS 
                tasks(
                    id integer PRIMARY KEY AUTOINCREMENT, 
                    task varchar(50) NOT NULL, 
                    due_date varchar(50), 
                    completed BOOLEAN NOT NULL CHECK (
                        completed IN (0, 1)
                    ),
                    priority int,
                    category varchar(50)
                )
            """
        )
        self.con.commit()
        

    def create_task(self, task, priority, due_date=None, category=""):
        self.cursor.execute(
            """
            INSERT INTO tasks(
                task, due_date, completed, priority, category 
            ) VALUES(?, ?, ?, ?, ?)
            """, 
            (task, due_date, 0, priority, category)
        )
        self.con.commit()

        created_task = self.cursor.execute(
            """
            SELECT 
                id, task, due_date, completed, priority, category 
            FROM tasks 
            WHERE 
                task = ? and completed = 0
            """, 
            (task,)
        ).fetchall()
        return created_task[-1]

    def get_tasks(self):
        today = datetime.now().strftime("%Y/%m/%d")
        uncomplete_tasks = self.get_ordered_uncomplete_tasks()
        completed_tasks = self.cursor.execute(
            f"""
            SELECT 
                id, task, due_date, completed, priority, category 
            FROM tasks 
            WHERE 
                completed = 1 and due_date >= '{today}'
            """
        ).fetchall()
        
        return completed_tasks, uncomplete_tasks
    
    def get_tasks_by_date(self, date):
        date = date.strftime('%Y/%m/%d')
        uncomplete_tasks = self.cursor.execute(
            f"""
            SELECT 
                id, task, due_date, completed, priority, category 
            FROM tasks 
            WHERE 
                completed = 0 and due_date = '{date}'
            """
        ).fetchall()
        completed_tasks = self.cursor.execute(
            f"""
            SELECT 
                id, task, due_date, completed, priority, category 
            FROM tasks 
            WHERE 
                completed = 1 and due_date = '{date}'
            """
        ).fetchall()
        print(uncomplete_tasks)
        return completed_tasks, uncomplete_tasks
    
    def get_ordered_uncomplete_tasks(self, type="date"):
        if type == "Priority":
            col = "priority"
            ord = "DESC"
        else:
            col = "due_date"
            ord = "ASC"

        tasks = self.cursor.execute(
            f"""
            SELECT 
                id, task, due_date, completed, priority, category 
            FROM tasks 
            WHERE 
                completed = 0
            ORDER BY {col} {ord}
            """
        ).fetchall()

        return tasks
    
    def get_category_list(self):
        category_list = self.cursor.execute(
            f"""
            SELECT 
                distinct category 
            FROM tasks 
            """
        ).fetchall()

        return category_list

    def mark_task_as_complete(self, taskid):
        self.cursor.execute(
            """
            UPDATE tasks 
            SET completed=1 
            WHERE id=?
            """, 
            (taskid,)
        )
        self.con.commit()

    def mark_task_as_incomplete(self, taskid):
        self.cursor.execute(
            """
            UPDATE tasks 
            SET completed=0 
            WHERE id=?
            """, 
            (taskid,)
        )
        self.con.commit()

        task_text = self.cursor.execute(
            """
            SELECT task 
            FROM tasks 
            WHERE id=?
            """, 
            (taskid,)
        ).fetchall()
        return task_text[0][0]

    def delete_task(self, taskid):
        self.cursor.execute(
            """
            DELETE FROM tasks 
            WHERE id=?
            """, 
            (taskid,)
        )
        self.con.commit()