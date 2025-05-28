import pytest

from utils.api_client import api
from utils.db_client import DbClient


@pytest.mark.api_comment
def test_delete_comment(data_and_create_comment):
    # 1. Формирование тестовых данных
    data_comment, post_id = data_and_create_comment

    # 2. Создание комментария
    response_create = api.post("/wp/v2/comments", data_comment)
    comment_id = response_create.json()["id"]

    # 3. Удаление комментария в корзину
    response_delete = api.delete(f"/wp/v2/comments/{comment_id}")

    # 4. Проверка статус-кода
    assert response_delete.status_code == 200

    # 5. Проверка в БД
    with DbClient() as dbc:
        db_response = dbc.query(f"SELECT * FROM wp_comments WHERE comment_ID = {comment_id}")

    assert db_response is not None, "Запрос не вернул данные"
    assert len(db_response) == 1, f"Запрос вернул {len(db_response)} записей. Ожидалось 1"

    # 6. Проверка значения атрибута status
    assert db_response[0]["comment_approved"] == "trash", "Комментарий не удален"

    # 7. Удаление комментария из БД
    response_delete = api.delete(endpoint=f"/wp/v2/comments/{comment_id}", json={"force": True})
    assert response_delete.status_code == 200

    with DbClient() as dbc:
        db_response = dbc.query(f"SELECT * FROM wp_comments WHERE comment_ID = {comment_id}")

    # 8. Проверка удаления комментария из БД
    assert len(db_response) == 0, "Комментарий не удален"
