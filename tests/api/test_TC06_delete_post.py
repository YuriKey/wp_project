import allure
import pytest

from utils.db_client import PostClient as pc


@allure.feature("Пост")
@allure.story("Удаление поста")
@allure.title("Проверка удаления поста / positive")
@pytest.mark.api_post
def test_delete_post(data_and_create_post, posts_api):
    post_id = data_and_create_post[1]

    with allure.step("1. Удаление поста через API"):
        posts_api.delete_post(post_id)

    with allure.step("2. Поиск удаленного пользователя в БД"):
        db_response = pc.get_post_status(post_id)

    with allure.step("3. Проверка значения атрибута 'status'"):
        assert db_response["post_status"] == "trash"
