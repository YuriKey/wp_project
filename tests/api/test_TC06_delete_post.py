import allure
import pytest

from utils.db_client import db_post_query as dpq


@allure.feature("Пост")
@allure.story("Удаление поста")
@allure.title("Проверка удаления поста / positive")
@pytest.mark.api_post
def test_delete_post(data_and_create_post, posts_api):
    with allure.step("1. Формирование тестовых данных"):
        post_id = data_and_create_post[1]

    with allure.step("2. Удаление поста через API"):
        posts_api.delete_post(post_id)

    with allure.step("3. Поиск удаленного пользователя в БД"):
        db_response = dpq.get_post_status(post_id)

    with allure.step("4. Проверка значения атрибута 'status'"):
        assert db_response["post_status"] == "trash"
