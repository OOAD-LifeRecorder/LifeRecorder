import sqlite3
from abc import ABC, abstractmethod

class Database(ABC):
    def __init__(self):
        self.con = sqlite3.connect(f'LifeRecorder.db')
        self.cursor = self.con.cursor()
        self._create_table()

    @abstractmethod
    def _create_table(self):
        pass

    def close_db_connection(self):
        self.con.close()
