import pytest

from utils.api_client import api
from utils.db_client import DbClient


@pytest.mark.api_comment
def test_create_comment(data_and_create_comment):
    # 1. Формирование тестовых данных
    expected_data, post_id = data_and_create_comment

    # 2. Создание комментария
    response = api.post("/wp/v2/comments", expected_data)

    comment_id = response.json()["id"]
    # 3. Проверка статус-кода
    assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}."

    # 4. Проверка данных в БД
    with DbClient() as dbc:
        db_response = dbc.query(
            f"SELECT * FROM wp_comments WHERE comment_ID = {comment_id}"
        )
    assert db_response is not None, f"Запрос в БД не вернул данных."
    assert len(db_response) == 1, f"Запрос в БД вернул {len(db_response)} записей, ожидалось 1."

    # 5. Сравнение данных
    actual_data = {
        "post": db_response[0]["comment_post_ID"],
        "content": db_response[0]["comment_content"]
    }

    assert actual_data["post"] == expected_data["post"], "ID поста не совпадают."
    assert actual_data["content"] == expected_data["content"], "Содержания не совпадают."
