import allure
import pytest

from utils.db_client import UserClient as uc


@allure.feature("Пользователь")
@allure.story("Удаление пользователя")
@allure.title("Проверка Удаления пользователя / positive")
@pytest.mark.api_user
def test_delete_user(data_and_create_user, users_api):
    expected_data, user_id = data_and_create_user

    with allure.step("1. Удаление пользователя через API"):
        users_api.delete_user(user_id)

    with allure.step("2. Проверка отсутствия пользователя в БД"):
        db_response = uc.check_is_deleted(user_id)
        assert db_response == 0, "Пользователь найден в БД"
