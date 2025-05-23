import pymysql
import pytest


def test_db_connection(db_connection):
    """Проверяет соединение с MySQL-контейнером ('db-1')."""
    print("\n>>> Начало теста: проверка соединения с БД...")
    connection = None
    try:
        # Проверяем, что соединение активно
        assert db_connection.open, "Соединение не установлено"
        print(">>> Соединение установлено. \nПроверяем таблицы...")

        # Проверяем доступ к таблицам
        with db_connection.cursor() as cursor:
            cursor.execute("SHOW TABLES FROM wordpress;")
            result = cursor.fetchone()
            print(f">>> Результат запроса: {result}")
            assert result, "Таблица wp_posts не найдена"

        print("✅  Соединение с БД успешно. Таблицы доступны.")

    except pymysql.Error as e:
        pytest.fail(f"Ошибка подключения: {e}")


def test_query(db_connection):
    """Проверяет количество пользователей в таблице wp_users."""
    print("\n>>> Начало теста: проверка количества пользователей...")

    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS count FROM wp_users")
        result = cursor.fetchone()
        print(f'\nРезультат запроса: {result}')
        assert result['count'] > 0, "Нет пользователей в таблице users"
        print("✅  Таблица wp_users содержит пользователей.")
