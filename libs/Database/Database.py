import sqlite3
from abc import ABC, abstractmethod

class Database(ABC):
    def __init__(self):
        self.db_name = self._get_db_name()
        self.con = sqlite3.connect(f'{self.db_name}.db')
        self.cursor = self.con.cursor()
        self._create_table()

    @abstractmethod
    def _get_db_name(self):
        pass

    @abstractmethod
    def _create_table(self):
        pass

    def close_db_connection(self):
        self.con.close()
