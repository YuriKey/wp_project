import pytest

from utils.api_client import api
from utils.db_client import DbClient


@pytest.mark.api_post
def test_update_post(data_and_create_post):
    # 1. Формирование тестовых данных
    old_data, post_id = data_and_create_post
    new_data = {
        "title": "Cats are awesome",
        "content": "Coons also are awesome, but not such as cats."
    }

    # 2. Обновление поста через API
    response = api.post(endpoint=f"/wp/v2/posts/{post_id}", json=new_data)

    # 3. Проверка статус-кода
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    # 4. Проверка изменения поста в БД
    with DbClient() as dbc:
        db_response = dbc.query(
            "SELECT * FROM wp_posts WHERE ID = ?",
            post_id
        )
    assert db_response is not None, "Запрос к БД не вернул результатов"
    assert len(db_response) == 1, f"Запрос в БД вернул {len(db_response)} записей, ожидалось 1."

    # 5. Сравнение данных
    actual_data = {
        "title": db_response[0]["post_title"],
        "content": db_response[0]["post_content"]
    }

    assert actual_data["title"] != old_data["post_title"], "Заголовок не изменился"
    assert actual_data["content"] != old_data["post_content"], "Содержание не изменилось"
    assert actual_data["title"] == new_data["title"], "Заголовок не изменился"
    assert actual_data["content"] == new_data["content"], "Содержание не изменилось"
