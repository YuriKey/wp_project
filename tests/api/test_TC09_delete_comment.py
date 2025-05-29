import allure
import pytest

from utils.db_client import db_comment_query as dcq


@allure.feature("Комментарий")
@allure.story("Удаление комментария")
@allure.title("Проверка удаления комментария / positive")
@pytest.mark.api_comment
def test_delete_comment(data_and_create_comment, comments_api):
    with allure.step("1. Формирование тестовых данных"):
        data_comment, post_id = data_and_create_comment

    with allure.step("2. Создание комментария"):
        response_create = comments_api.create_comment(data_comment)
        comment_id = response_create.json()["id"]

    with allure.step("3. Удаление комментария в корзину"):
        comments_api.delete_comment(comment_id)

    with allure.step("4. Поиск удаленного комментария в БД"):
        db_response = dcq.get_comment_data(comment_id)

    with allure.step("5. Проверка значения атрибута status"):
        assert db_response["comment_approved"] == "trash", "Комментарий не удален"

    with allure.step("6. Удаление комментария из БД"):
        comments_api.delete_comment(comment_id, data={"force": True})

    with allure.step("7. Поиск удаленного комментария в БД"):
        db_response_delete = dcq.check_is_deleted(comment_id)
        assert db_response_delete == 0, "Комментарий не удален"
