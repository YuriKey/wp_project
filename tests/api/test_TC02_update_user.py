import allure
import pytest

from data.generators.user_data_generators import UsersData as ud
from utils.db_client import UserClient as uc


@allure.feature("Пользователь")
@allure.story("Обновление пользователя")
@allure.title("Проверка обновления пользователя / positive")
@pytest.mark.api_user
def test_update_user(data_and_delete_user, users_api):
    user_id, old_user_data = data_and_delete_user
    new_data = ud.create_user_data_without_username()

    with allure.step("1. Создание пользователя и получение его ID"):
        response = users_api.create_user(old_user_data)
        user_id["id"] = response.json()["id"]

    with allure.step("2. Обновление пользователя через API"):
        users_api.update_user(user_id["id"], new_data)

    with allure.step("3. Поиск измененного пользователя в БД"):
        user_db = uc.get_user_with_meta(user_id["id"])

    with allure.step("4. Сравнение ответа из БД с ожидаемыми данными"):
        assert user_db.user_login == old_user_data["username"], "Произошло обновление поля readonly (user_login)."
        assert user_db.user_email == new_data["email"], "Поле user_email не было обновлено"
        assert user_db.display_name == new_data["name"], "Поле name не было обновлено"
        assert user_db.last_name == new_data.get("last_name", ""), "Поле last_name не было обновлено"
