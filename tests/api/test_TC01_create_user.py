import allure
import pytest

from utils.db_client import UserClient as uc


@allure.feature("Пользователь")
@allure.story("Создание пользователя")
@allure.title("Проверка создания пользователя / positive")
@pytest.mark.api_user
def test_create_user(data_and_delete_user, users_api):
    user_id, expected_data = data_and_delete_user

    with allure.step("1. Создание пользователя через API"):
        response = users_api.create_user(expected_data)

    with allure.step("2. Получение ID созданного пользователя"):
        user_id["id"] = response.json().get("id")

    with allure.step("3. Поиск в пользователя в БД"):
        db_response = uc.get_login_email(user_id["id"])

    with allure.step("4. Сравнение отправленных и полученных данных"):
        assert db_response.user_login == expected_data["username"], "Логин не совпадает"
        assert db_response.user_email == expected_data["email"], "Email не совпадает"
