import allure
import pytest

from utils.db_client import db_post_query as dpq


@allure.feature("Пост")
@allure.story("Создание поста")
@allure.title("Проверка создания поста / positive")
@pytest.mark.api_post
def test_create_post(title_and_delete_post, posts_api):
    with allure.step("1. Формирование тестовых данных"):
        post_id, expected_title = title_and_delete_post

    with allure.step("2. Создание поста через API"):
        response = posts_api.create_post(expected_title)
        post_id["id"] = response.json().get("id", None)

    with allure.step("3. Поиск в БД"):
        db_response = dpq.get_post_title(post_id["id"])

    with allure.step("4. Сравнение ожидаемых и фактических результатов"):
        assert expected_title["title"] == db_response["post_title"]
