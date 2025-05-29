import allure
import pytest

from utils.db_client import db_post_query as dpq


@allure.feature("Пост")
@allure.story("Обновление поста")
@allure.title("Проверка обновления поста / positive")
@pytest.mark.api_post
def test_update_post(data_and_create_post, posts_api):
    with allure.step("1. Формирование тестовых данных"):
        old_data, post_id = data_and_create_post

        new_data = {
            "title": "Cats are awesome",
            "content": "Coons also are awesome, but not such as cats."
        }

    with allure.step("2. Обновление поста через API"):
        posts_api.update_post(post_id, new_data)

    with allure.step("3. Поиск измененного поста в БД"):
        db_response = dpq.get_post_data(post_id)

    with allure.step("4. Сравненение ответа из БД с ожидаемыми данными"):
        assert db_response["title"] != old_data["post_title"], "Заголовок не изменился"
        assert db_response["content"] != old_data["post_content"], "Содержание не изменилось"
        assert db_response["title"] == new_data["title"], "Заголовок не изменился"
        assert db_response["content"] == new_data["content"], "Содержание не изменилось"
