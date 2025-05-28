import pytest

from utils.api_client import api
from utils.db_client import DbClient


@pytest.mark.api_user
def test_delete_user(data_and_create_user):
    # 1. Запрос тестовых данных из фикстуры
    expected_data, user_id = data_and_create_user

    # 2. Удаление пользователя через API
    response = api.delete(f"/wp/v2/users/{user_id}", json={"reassign": "1", "force": "true"})

    # 3. Проверка статус-кода
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    # 4. Проверка в БД
    with DbClient() as dbc:
        db_response = dbc.query(
            "SELECT user_login, user_email FROM wp_users WHERE ID = ?",
            (user_id,)
        )

    assert db_response is not None, "Запрос к БД не вернул результатов"
    assert len(db_response) == 0, "Пользователь найден в БД"
