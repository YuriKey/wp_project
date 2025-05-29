import pytest
from tests.api.conftest import db
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()])

logger = logging.getLogger(__name__)


@pytest.mark.service
def test_db_connection(db):
    """Проверка подключения к БД через ODBC."""
    try:
        result = db.query("SHOW TABLES FROM wordpress;")
        assert result, "Таблица wp_posts не найдена"
        logger.info("Подключение к БД успешно.")
    except Exception as e:
        logger.error(f"Ошибка при подключении к БД: {e}")
        raise


@pytest.mark.service
def test_another(db):
    """Проверка запроса к таблице wp_comments."""
    try:
        result = db.query("SELECT * FROM wp_comments;")
        assert result, "Таблица wp_users не найдена"
        logger.info("Запрос к таблице wp_comments выполнен успешно!")
    except Exception as e:
        logger.error(f"Ошибка при выполнении запроса к wp_comments: {e}")
        raise
