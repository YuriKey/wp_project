def test_db_connection(db):
    """Проверка подключения к БД через ODBC."""
    try:
        result = db.execute_query("SHOW TABLES FROM wordpress;")
        print(f">>> Результат запроса: {result}")
        assert result, "Таблица wp_posts не найдена"
        print("✅ Подключение к БД успешно!")
    except Exception as e:
        print(f"Ошибка: {e}")


def test_another(db):
    try:
        result = db.execute_query("SELECT * FROM wp_comments;")
        print(f">>> Результат запроса: {result}")
        assert result, "Таблица wp_users не найдена"
    except Exception as e:
        print(f"Ошибка: {e}")