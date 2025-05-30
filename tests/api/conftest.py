# conftest.py
import pytest
from faker import Faker

from config.api_config import BASE_URL
from data.generators.comment_data_generators import generated_comment_data as gcd
from data.generators.post_data_generators import generated_post_data as gpd
from data.generators.user_data_generators import generated_user_data as gud
from utils.api_client import UsersApi, PostsApi, CommentsApi
from utils.db_client import DbClient

fake = Faker()


@pytest.fixture(scope="session")
def db():
    """Фикстура для тестов с БД."""
    client = DbClient()
    yield client


@pytest.fixture
def comments_api():
    return CommentsApi(BASE_URL)


@pytest.fixture
def posts_api():
    return PostsApi(BASE_URL)


@pytest.fixture
def users_api():
    return UsersApi(BASE_URL)


@pytest.fixture(scope="function")
def data_and_delete_user():
    """
    Возвращает сгенерированную user_data и пустой словарь для user_id перед тестом.
    Удаляет пользователя после теста.
    """
    user_id = {"id": None}
    expected_data = gud.create_minimal_user_data()

    yield user_id, expected_data
    if user_id["id"]:
        with DbClient() as dbc:
            dbc.execute("DELETE FROM wp_users WHERE ID = ?", (user_id["id"],))


@pytest.fixture(scope="function")
def data_and_create_user():
    """
    Возвращает сгенерированную user_data и user_id перед тестом.
    """
    expected_data = gud.create_full_user_data()

    with DbClient() as dbc:
        dbc.execute("""INSERT INTO wp_users (
                    user_pass, 
                    user_email,
                    display_name, 
                    user_registered, 
                    user_login, 
                    user_nicename) 
                    VALUES (?, ?, ?, ?, ?, ?)""",
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
    Возвращает сгенерированную post_title и пустой словарь для post_id перед тестом.
    Удаляет пост после теста.
    """
    post_id = {"id": None}
    post_data = gpd.generate_minimal_post_data()
    yield post_id, post_data
    if post_id["id"]:
        with DbClient() as dbc:
            dbc.execute("DELETE FROM wp_posts WHERE ID = ?", (post_id["id"],))


@pytest.fixture(scope="function")
def data_and_create_post():
    """
    Возвращает сгенерированную post_data и post_id перед тестом.
    """
    post_data = gpd.generate_full_post_data()

    with DbClient() as dbc:
        dbc.query(
            """INSERT INTO wp_posts(
            post_title,
            post_date,
            post_date_gmt,
            post_modified,
            post_modified_gmt,
            post_content,
            post_excerpt,
            to_ping,
            pinged,
            post_content_filtered)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            (post_data["post_title"],
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

    data_comment = gcd.generate_comment_data(post_id)

    return data_comment, post_id
