import allure
import pytest

from utils.db_client import CommentClient as cc


@allure.feature("Комментарий")
@allure.story("Создание комментария")
@allure.title("Проверка создания комментария / positive")
@pytest.mark.api_comment
def test_create_comment(data_and_create_comment, comments_api):
    expected_data, post_id = data_and_create_comment

    with allure.step("1. Создание комментария"):
        response = comments_api.create_comment(expected_data)
        comment_id = response.json()["id"]

    with allure.step("2. Поиск комментария в БД"):
        db_response = cc.get_comment_data(comment_id)

    with allure.step("3. Сравненение ответа из БД с ожидаемыми данными"):
        assert db_response["comment_post_ID"] == expected_data["post"], "ID поста не совпадают."
        assert db_response["comment_content"] == expected_data["content"], "Содержания не совпадают."
