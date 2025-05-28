import pytest

from utils.api_client import api
from utils.db_client import DbClient


@pytest.mark.api_user
def test_create_user(data_and_delete_user):
    # 1. Запрос тестовых данных из фикстуры
    user_id_, expected_data = data_and_delete_user

    # 2. Создание пользователя через API
    response = api.post("/wp/v2/users", json=expected_data)

    # 3. Проверка статус-кода
    assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"

    # 4. Получение ID созданного пользователя
    user_id_["id"] = response.json().get("id")  # Передаем ID в фикстуру для удаления после теста.

    # 5. Проверка в БД
    with DbClient() as dbc:
        db_response = dbc.query(
            "SELECT user_login, user_email FROM wp_users WHERE ID = ?",
            (user_id_["id"],)
        )

    assert db_response is not None, "Запрос к БД не вернул результатов"
    assert len(db_response) == 1, "Пользователь не найден в БД"

    # 6. Сравнение данных
    actual_data = {
        "username": db_response[0]["user_login"],
        "email": db_response[0]["user_email"]
    }

    assert actual_data["username"] == expected_data["username"]
    assert actual_data["email"] == expected_data["email"]
