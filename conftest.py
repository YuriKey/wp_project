# conftest.py
import pytest
from utils.db_client import DBClient


@pytest.fixture(scope="session")
def db():
    """Фикстура для тестов с БД."""
    client = DBClient()
    yield client
    client.close()
