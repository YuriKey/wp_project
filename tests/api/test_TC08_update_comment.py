import allure
import pytest

from data.generators.comment_data_generators import CommentData as cd
from utils.db_client import CommentClient as cc


@allure.feature("Комментарий")
@allure.story("Обновление комментария")
@allure.title("Проверка обновления комментария / positive")
@pytest.mark.api_comment
def test_update_comment(data_and_create_comment, comments_api):
    old_data, post_id = data_and_create_comment
    new_data = cd.generate_comment_data_author()

    with allure.step("1. Создание комментария"):
        response_create = comments_api.create_comment(old_data)
        comment_id = response_create.json()["id"]

    with allure.step("2. Изменение комментария"):
        comments_api.update_comment(comment_id, new_data)

    with allure.step("3. Поиск измененного комментария в БД"):
        db_response = cc.get_comment_data(comment_id)

    with allure.step("4. Сравненение ответа из БД с ожидаемыми данными"):
        assert db_response["comment_post_ID"] == old_data["post"], "ID поста не совпадает"
        assert db_response["comment_content"] == new_data["content"], "Содержимое комментария не совпадает"
        assert db_response["comment_author"] == new_data["author_name"], "Имя автора не совпадает"
