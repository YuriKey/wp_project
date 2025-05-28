import os

import pytest

from config.test_config import SQL_SCRIPTS_DIR
from utils.api_client import api
from utils.db_client import DbClient


@pytest.mark.api_user
def test_update_user(data_and_delete_user):
    # 1. Формирование тестовых данных
    user_id, old_user_data = data_and_delete_user

    new_data = {
        "name": "Chuck",  # wp_users.display_name
        "email": "chuck@awesome.com",  # wp_users.user_email
        "password": "123456",
        "last_name": "Norris"  # meta_users.last_name
    }

    # 2. Создание пользователя и получение его ID
    response = api.post("/wp/v2/users", json=old_user_data)
    user_id["id"] = response.json()["id"]

    # 3. Обновление пользователя через API
    response_update = api.post(f"/wp/v2/users/{user_id['id']}", json=new_data)

    # 4. Проверка статус-кода
    assert response_update.status_code == 200, "Пользователь не был обновлен"

    # 5. Проверка в БД
    sql_path = os.path.join(SQL_SCRIPTS_DIR, "get_user_with_meta.sql")
    with open(sql_path, "r") as script:
        sql_query = script.read()

    with DbClient() as dbc:
        db_response = dbc.query(
            sql_query,
            params=(user_id["id"],)
        )

    assert db_response is not None, "Запрос к БД не вернул результатов"
    assert len(db_response) == 1, "Пользователь не найден в БД"

    # 6. Сравнение данных
    actual_data = {
        "user_login": db_response[0]["user_login"],
        "name": db_response[0]["display_name"],
        "user_email": db_response[0]["user_email"],
        "last_name": db_response[0]["last_name"]
    }

    assert actual_data["user_login"] == old_user_data["username"], "Произошло обновление поля readonly (user_login)."
    assert actual_data["user_email"] == new_data["email"], "Поле user_email не было обновлено"
    assert actual_data["name"] == new_data["name"], "Поле name не было обновлено"
    assert actual_data["last_name"] == new_data.get("last_name", ""), "Поле last_name не было обновлено"
