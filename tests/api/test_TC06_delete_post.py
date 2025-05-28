import pytest

from utils.api_client import api
from utils.db_client import DbClient


@pytest.mark.api_post
def test_delete_post(data_and_create_post):
    # 1. Формирование тестовых данных
    post_id = data_and_create_post[1]

    # 2. Удаление поста через API
    response = api.delete(f"/wp/v2/posts/{post_id}")

    # 3. Проверка статус-кода
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    # 4. Проверка БД
    with DbClient() as dbc:
        db_response = dbc.query(
            "SELECT * FROM wp_posts WHERE ID = ?",
            post_id)

    # 5. Проверка значения атрибута "status", должно быть "trash"
    assert db_response[0]["post_status"] == "trash"
