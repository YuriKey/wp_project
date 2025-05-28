import pyodbc

from config.db_config import CONNECT_STRING


class DbClient:
    def __init__(self):
        self.connection = pyodbc.connect(CONNECT_STRING)

    def query(self, sql: str, params=None) -> list[dict] | None:
        """Выполняет SQL-запрос и возвращает результат в виде списка словарей (SELECT)"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params or ())  # Заменили {} на ()
            if cursor.description:  # Если есть результаты
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            return None

    def execute(self, sql: str, params=None) -> None:
        """Выполняет SQL-команду без возврата результатов (INSERT/UPDATE/DELETE)"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params or ())
            self.connection.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
