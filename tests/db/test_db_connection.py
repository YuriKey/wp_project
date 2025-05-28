import pytest


@pytest.mark.service
def test_db_connection(db):
    """Проверка подключения к БД через ODBC."""
    try:
        result = db.query("SHOW TABLES FROM wordpress;")
        assert result, "Таблица wp_posts не найдена"
        print("✅ Подключение к БД успешно!")
    except Exception as e:
        print(f"Ошибка: {e}")


@pytest.mark.service
def test_another(db):
    try:
        result = db.query("SELECT * FROM wp_comments;")
        assert result, "Таблица wp_users не найдена"
    except Exception as e:
        print(f"Ошибка: {e}")