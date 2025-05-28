# conftest.py
import os
import pytest
from faker import Faker

from utils.db_client import DbClient
from config.test_config import SQL_SCRIPTS_DIR

fake = Faker()


@pytest.fixture(scope="session")
def db():
    """Фикстура для тестов с БД."""
    client = DbClient()
    yield client


@pytest.fixture(scope="function")
def data_and_delete_user():
    """
    Возвращает сгенерированную user_data и пустой словарь для user_id перед тестом.
    Удаляет пользователя после теста.
    """
    user_id = {"id": None}  # Используем словарь для хранения ID, словари мутируемы.
    username = fake.user_name()
    expected_data = {
        "username": f"{username}",
        "email": f"{username}@{fake.domain_name()}",
        "password": f"{fake.password()}"
    }

    yield user_id, expected_data  # Передаём словари в тест
    if user_id["id"]:
        with DbClient() as dbc:
            dbc.execute("DELETE FROM wp_users WHERE ID = ?", (user_id["id"],))


@pytest.fixture(scope="function")
def data_and_create_user():
    """
    Возвращает сгенерированную user_data и user_id перед тестом.
    """
    username = fake.user_name()
    expected_data = {
        "username": f"{username}",
        "login": f"{username}.{fake.last_name()}",
        "user_nicename": f"{fake.first_name()}",
        "email": f"{username}@{fake.domain_name()}",
        "password": f"{fake.password()}"
    }
    with DbClient() as dbc:
        dbc.execute("INSERT INTO wp_users "
                    "(user_pass, user_email, display_name, user_registered, user_login, user_nicename) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (expected_data["password"],
                     expected_data["email"],
                     expected_data["username"],
                     fake.date_time(),
                     expected_data["login"],
                     expected_data["user_nicename"]
                     )),
        user_id = dbc.query("SELECT ID FROM wp_users WHERE user_login = ?", (expected_data["login"],)),

        return expected_data, user_id[0][0]["ID"]


@pytest.fixture(scope="function")
def title_and_delete_post():
    """
    TODO: добавить  post_content?
    Возвращает сгенерированную post_title и пустой словарь для post_id перед тестом.
    Удаляет пост после теста.
    """
    post_id = {"id": None}
    post_title = fake.text(max_nb_chars=60)

    yield post_id, post_title
    if post_id["id"]:
        with DbClient() as dbc:
            dbc.execute("DELETE FROM wp_posts WHERE ID = ?", (post_id["id"],))


@pytest.fixture(scope="function")
def data_and_create_post():
    """
    Возвращает сгенерированную post_data и post_id перед тестом.
    """
    post_data = {
        "post_title": fake.text(max_nb_chars=60),
        "post_date": fake.date_time(),
        "post_date_gmt": fake.date_time(),
        "post_modified": fake.date_time(),
        "post_modified_gmt": fake.date_time(),
        "post_content": fake.text(max_nb_chars=1000),
        "post_excerpt": fake.text(max_nb_chars=100),
        "to_ping": fake.url(),
        "pinged": fake.url(),
        "post_content_filtered": fake.text(max_nb_chars=1000)
    }

    sql_path = os.path.join(SQL_SCRIPTS_DIR, "create_post.sql")
    with open(sql_path, "r") as script:
        sql_query = script.read()

    with DbClient() as dbc:
        dbc.query(
            sql_query,
            params=(post_data["post_title"],
                    post_data["post_date"],
                    post_data["post_date_gmt"],
                    post_data["post_modified"],
                    post_data["post_modified_gmt"],
                    post_data["post_content"],
                    post_data["post_excerpt"],
                    post_data["to_ping"],
                    post_data["pinged"],
                    post_data["post_content_filtered"]
                    )
        ),
        post_id = dbc.query(
            "SELECT ID FROM wp_posts WHERE post_title = ?",
            (post_data["post_title"],)
        )

    return post_data, post_id[0]["ID"]


@pytest.fixture(scope="function")
def data_and_create_comment(data_and_create_post):
    """
    Возвращает сгенерированную comment_data и post_id перед тестом.
    """
    post_id = data_and_create_post[1]

    data_comment = {
        "post": post_id,
        "content": fake.text(max_nb_chars=150)
    }

    return data_comment, post_id
