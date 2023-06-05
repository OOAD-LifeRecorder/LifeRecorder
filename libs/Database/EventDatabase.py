from libs.Database.Database import Database
from datetime import datetime

class EventDatabase(Database):
    def _get_db_name(self):
        return "event"

    def _create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS 
                events(
                    id integer PRIMARY KEY AUTOINCREMENT, 
                    name varchar(50) NOT NULL, 
                    due_date varchar(50), 
                    category BOOLEAN NOT NULL
                )
            """
        )
        self.con.commit()
        

    def create_event(self, name, due_date, category=0):
        self.cursor.execute(
            """
            INSERT INTO events(
                name, due_date, category
            ) VALUES(?, ?, ?)
            """, 
            (name, due_date, category)
        )
        self.con.commit()

        created_event = self.cursor.execute(
            """
            SELECT 
                id, name, due_date, category 
            FROM events
            WHERE 
                name = ?
            """, 
            (name,)
        ).fetchall()
        return created_event[-1]

    def get_events_by_date(self, date):
        events = self.cursor.execute(
            f"""
            SELECT 
                id, name, category
            FROM events 
            WHERE due_date = '{date}'
            """
        ).fetchall()
        return events

    def delete_event(self, event_id):
        self.cursor.execute(
            """
            DELETE FROM events 
            WHERE id=?
            """, 
            (event_id,)
        )
        self.con.commit()