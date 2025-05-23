# Класс для работы с БД (PyMySQL/SQLAlchemy)
import pymysql
from pymysql.cursors import DictCursor


class DbClient:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=DictCursor
        )

    def query(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def close(self):
        self.connection.close()
