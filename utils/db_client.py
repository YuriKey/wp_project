# utils/db_client.py
import pyodbc
from config.db_config import CONNECT_STRING


class DBClient:
    def __init__(self):
        self.conn = pyodbc.connect(CONNECT_STRING)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        """Выполняет SELECT-запрос и возвращает результат"""
        self.cursor.execute(query, params) if params else self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute_non_query(self, query, params=None):
        """Выполняет INSERT/UPDATE/DELETE-запросы"""
        self.cursor.execute(query, params) if params else self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
