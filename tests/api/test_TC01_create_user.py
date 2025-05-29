import allure
import pytest

from utils.db_client import db_user_query as duq


@allure.feature("Пользователь")
@allure.story("Создание пользователя")
@allure.title("Проверка создания пользователя / positive")
@pytest.mark.api_user
def test_create_user(data_and_delete_user, users_api):
    with allure.step("1. Запрос тестовых данных из фикстуры"):
        user_id, expected_data = data_and_delete_user

    with allure.step("2. Создание пользователя через API"):
        response = users_api.create_user(expected_data)

    with allure.step("3. Получение ID созданного пользователя"):
        user_id["id"] = response.json().get("id")

    with allure.step("4. Поиск в пользователя в БД"):
        db_response = duq.get_login_email(user_id["id"])

    with allure.step("5. Сравнение отправленных и полученных данных"):
        assert db_response["username"] == expected_data["username"]
        assert db_response["email"] == expected_data["email"]
