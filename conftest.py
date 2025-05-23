# tests/db/conftest.py

import pytest
import pymysql


@pytest.fixture(scope="session")
def db_connection():
    """Фикстура для подключения к бд."""
    connection = None
    try:
        # Загрузка конфигурации из файла config/config.py
        from config.config import DB_CONFIG

        # Подключаемся к БД
        connection = pymysql.connect(
            **DB_CONFIG)
        yield connection
    finally:
        if connection:
            connection.close()
