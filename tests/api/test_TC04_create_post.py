import pytest

from utils.api_client import api
from utils.db_client import DbClient


@pytest.mark.api_post
def test_create_post(title_and_delete_post):
    # 1. Запрос тестовых данных из фикстуры
    post_id, expected_title = title_and_delete_post

    # 2. Создание поста через API
    response = api.post("/wp/v2/posts", json={"title": f"{expected_title}"})

    # 3. Проверка статус-кода
    assert response.status_code == 201, f"Ожидался статус-код 201, получен {response.status_code}"

    # 4. Получение ID созданного поста
    post_id["id"] = response.json().get("id", None)

    # 5. Проверка в БД
    with DbClient() as dbc:
        db_response = dbc.query(
            "SELECT post_title FROM wp_posts WHERE ID = ?",
            (post_id["id"],)
        )

    assert db_response is not None, "Запрос к БД не вернул результатов"
    assert len(db_response) == 1, "Пользователь не найден в БД"

    # 6. Сравнение заголовков
    assert expected_title == db_response[0]["post_title"]
