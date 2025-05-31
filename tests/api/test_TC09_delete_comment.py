import allure
import pytest

from utils.db_client import CommentClient as cc


@allure.feature("Комментарий")
@allure.story("Удаление комментария")
@allure.title("Проверка удаления комментария / positive")
@pytest.mark.api_comment
def test_delete_comment(data_and_create_comment, comments_api):
    data_comment, post_id = data_and_create_comment

    with allure.step("1. Создание комментария"):
        response_create = comments_api.create_comment(data_comment)
        comment_id = response_create.json()["id"]

    with allure.step("2. Удаление комментария в корзину"):
        comments_api.delete_comment(comment_id)

    with allure.step("3. Поиск удаленного комментария в БД"):
        db_response = cc.get_comment_data(comment_id)

    with allure.step("4. Проверка значения атрибута status"):
        assert db_response["comment_approved"] == "trash", "Комментарий не удален"

    with allure.step("5. Удаление комментария из БД"):
        comments_api.delete_comment(comment_id, data={"force": True})

    with allure.step("6. Поиск удаленного комментария в БД"):
        db_response_delete = cc.check_is_deleted(comment_id)
        assert db_response_delete == 0, "Комментарий не удален"
