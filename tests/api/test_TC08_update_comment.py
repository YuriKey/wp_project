import pytest

from utils.api_client import api
from utils.db_client import DbClient


@pytest.mark.api_comment
def test_update_comment(data_and_create_comment):
    # 1. Формирование тестовых данных
    old_data, post_id = data_and_create_comment

    new_data = {
        "content": "Hi there!",
        "author_name": "ben.kenobi"
    }

    # 2. Создание комментария
    response_create = api.post("/wp/v2/comments", old_data)

    comment_id = response_create.json()["id"]

    # 3. Изменение комментария
    response_update = api.post(f"/wp/v2/comments/{comment_id}", new_data)

    # 4. Проверка статус-кода
    assert response_update.status_code == 200, f"Ожидался статус-код 200, получен {response_update.status_code}"

    # 5. Проверка изменения комментария
    with DbClient() as dbc:
        db_response = dbc.query(f"SELECT * FROM wp_comments WHERE comment_ID = {comment_id}")

    assert db_response is not None, "Запрос к БД не вернул данных"
    assert len(db_response) == 1, f"Запрос в БД вернул {len(db_response)} записей, ожидалось 1."

    # 6. Сравнение данных
    actual_data = {
        "post": db_response[0]["comment_post_ID"],
        "content": db_response[0]["comment_content"],
        "author_name": db_response[0]["comment_author"]
    }

    assert actual_data["post"] == old_data["post"], "ID поста не совпадает"
    assert actual_data["content"] == new_data["content"], "Содержимое комментария не совпадает"
    assert actual_data["author_name"] == new_data["author_name"], "Имя автора не совпадает"
