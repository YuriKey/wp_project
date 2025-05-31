import allure
import pytest
from faker import Faker

from config.api_config import BASE_URL
from data.generators.comment_data_generators import CommentData
from data.generators.post_data_generators import PostData
from data.generators.user_data_generators import UsersData
from utils.api_client import UsersApi, PostsApi, CommentsApi
from utils.db_client import DbClient, UserClient as uc, PostClient as pc

fake = Faker()


@pytest.fixture(scope="session")
def db():
    """Фикстура для тестов с БД."""
    client = DbClient()
    yield client


@pytest.fixture
def users_data_generate():
    return UsersData


@pytest.fixture
def posts_data_generate():
    return PostData


@pytest.fixture
def comments_data_generate():
    return CommentData


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
def data_and_delete_user(users_api, users_data_generate):
    """
    Возвращает сгенерированную user_data и пустой словарь для user_id перед тестом.
    Удаляет пользователя после теста.
    """
    user_id = {"id": None}
    with allure.step("Предусловие: генерация минимальных данных пользователя"):
        expected_data = users_data_generate.create_minimal_user_data()

    yield user_id, expected_data
    if user_id["id"]:
        with allure.step("Постусловие: удаление пользователя"):
            users_api.delete_user(user_id["id"])


@pytest.fixture(scope="function")
def data_and_create_user(users_data_generate):
    """
    Возвращает сгенерированную user_data и user_id перед тестом.
    """
    with allure.step("Предусловие: генерация данных пользователя"):
        expected_data = users_data_generate.create_full_user_data()

    user_id = uc.db_create_user(expected_data)
    return expected_data, user_id


@pytest.fixture(scope="function")
def title_and_delete_post(posts_api, posts_data_generate):
    """
    Возвращает сгенерированную post_title и пустой словарь для post_id перед тестом.
    Удаляет пост после теста.
    """
    post_id = {"id": None}
    with allure.step("Предусловие: генерация минимальных данных"):
        post_data = posts_data_generate.generate_minimal_post_data()

    yield post_id, post_data
    if post_id["id"]:
        with allure.step("Постусловие: удаление поста"):
            posts_api.delete_post(post_id["id"])


@pytest.fixture(scope="function")
def data_and_create_post(posts_data_generate):
    """
    Возвращает сгенерированную post_data и post_id перед тестом.
    """
    with allure.step("Предусловие: генерация данных поста"):
        post_data = posts_data_generate.generate_full_post_data()

    post_id = pc.db_create_post(post_data)

    return post_data, post_id


@pytest.fixture(scope="function")
def data_and_create_comment(data_and_create_post, comments_data_generate):
    """
    Возвращает сгенерированную comment_data и post_id перед тестом.
    """
    with allure.step("Предусловие: создание поста, генерация данных комментария"):
        post_id = data_and_create_post[1]

        data_comment = comments_data_generate.generate_comment_data(post_id)

    return data_comment, post_id
