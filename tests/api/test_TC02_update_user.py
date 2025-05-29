import allure
import pytest

from utils.db_client import db_user_query as duq


@allure.feature("Пользователь")
@allure.story("Обновление пользователя")
@allure.title("Проверка обновления пользователя / positive")
@pytest.mark.api_user
def test_update_user(data_and_delete_user, users_api):
    with allure.step("1. Формирование тестовых данных"):
        user_id, old_user_data = data_and_delete_user

        new_data = {
            "name": "Chuck",
            "email": "chuck@awesome.com",
            "password": "123456",
            "last_name": "Norris"
        }

    with allure.step("2. Создание пользователя и получение его ID"):
        response = users_api.create_user(old_user_data)
        user_id["id"] = response.json()["id"]

    with allure.step("3. Обновление пользователя через API"):
        users_api.update_user(user_id["id"], new_data)

    with allure.step("4. Поиск измененного пользователя в БД"):
        db_response = duq.get_user_with_meta(user_id["id"], )

    with allure.step("5. Сравненение ответа из БД с ожидаемыми данными"):
        assert db_response["user_login"] == old_user_data[
            "username"], "Произошло обновление поля readonly (user_login)."
        assert db_response["user_email"] == new_data["email"], "Поле user_email не было обновлено"
        assert db_response["name"] == new_data["name"], "Поле name не было обновлено"
        assert db_response["last_name"] == new_data.get("last_name", ""), "Поле last_name не было обновлено"
