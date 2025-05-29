import pyodbc

from config.db_config import CONNECT_STRING


class DbClient:
    def __init__(self):
        self.connection = pyodbc.connect(CONNECT_STRING)

    def query(self, sql: str, params=None) -> list[dict] | None:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params or ())
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            return None

    def execute(self, sql: str, params=None) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params or ())
            self.connection.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class UserClient(DbClient):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_login_email(user_id):
        with DbClient() as dbc:
            db_response = dbc.query(
                "SELECT user_login, user_email FROM wp_users WHERE ID = ?",
                (user_id,)
            )

        assert db_response is not None, "Запрос к БД не вернул результатов"
        assert len(db_response) == 1, "Пользователь не найден в БД"

        query_result = {
            "username": db_response[0]["user_login"],
            "email": db_response[0]["user_email"]
        }
        return query_result

    @staticmethod
    def get_user_with_meta(user_id):

        with DbClient() as dbc:
            db_response = dbc.query(
                "SELECT DISTINCT "
                "u.ID, u.user_login, u.user_email, u.display_name, m.meta_value AS last_name "
                "FROM wp_users u "
                "JOIN wp_usermeta m "
                "ON u.ID = m.user_id AND m.meta_key = 'last_name' "
                "WHERE u.ID = ?;",
                params=(user_id,)
            )

        assert db_response is not None, "Запрос к БД не вернул результатов"
        assert len(db_response) == 1, "Пользователь не найден в БД"

        query_result = {
            "user_login": db_response[0]["user_login"],
            "name": db_response[0]["display_name"],
            "user_email": db_response[0]["user_email"],
            "last_name": db_response[0]["last_name"]
        }

        return query_result

    @staticmethod
    def check_is_deleted(user_id):
        with DbClient() as dbc:
            db_response = dbc.query(
                "SELECT COUNT(*) FROM wp_users WHERE ID = ?",
                (user_id,)
            )
            query_result = db_response[0]["COUNT(*)"]
        assert db_response is not None, "Запрос к БД не вернул результатов"

        return query_result


class PostClient(DbClient):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_post_title(post_id):
        with DbClient() as dbc:
            db_response = dbc.query(
                "SELECT post_title FROM wp_posts WHERE ID = ?",
                (post_id,)
            )
        assert db_response is not None, "Запрос к БД не вернул результатов"
        assert len(db_response) == 1, "Пост не найден в БД"

        query_result = {
            "post_title": db_response[0]["post_title"]
        }

        return query_result

    @staticmethod
    def get_post_data(post_id):
        with DbClient() as dbc:
            db_response = dbc.query(
                "SELECT * FROM wp_posts WHERE ID = ?",
                post_id
            )
        assert db_response is not None, "Запрос к БД не вернул результатов"
        assert len(db_response) == 1, f"Запрос в БД вернул {len(db_response)} записей, ожидалось 1."

        query_result = {
            "title": db_response[0]["post_title"],
            "content": db_response[0]["post_content"]
        }

        return query_result

    @staticmethod
    def get_post_status(post_id):
        with DbClient() as dbc:
            db_response = dbc.query(
                "SELECT post_status FROM wp_posts WHERE ID = ?",
                (post_id,)
            )
        assert db_response is not None, "Запрос к БД не вернул результатов"
        assert len(db_response) == 1, "Пост не найден в БД"

        query_result = {
            "post_status": db_response[0]["post_status"]
        }

        return query_result


class CommentClient(DbClient):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_comment_data(comment_id, fields: list = None):
        select_fields = ", ".join(fields) if fields else "*"

        with DbClient() as dbc:
            db_response = dbc.query(
                f"SELECT {select_fields} FROM wp_comments WHERE comment_ID = ?",
                (comment_id,)
            )
        assert db_response is not None, "Запрос к БД не вернул результатов"
        assert len(db_response) == 1, f"Запрос в БД вернул {len(db_response)} записей, ожидалось 1."

        query_result = db_response[0] if fields is None \
            else {field: db_response[0][field] for field in fields}

        return query_result

    @staticmethod
    def check_is_deleted(comment_id):
        with DbClient() as dbc:
            db_response = dbc.query(
                "SELECT COUNT(*) FROM wp_users WHERE ID = ?",
                (comment_id,)
            )
            query_result = db_response[0]["COUNT(*)"]
        assert db_response is not None, "Запрос к БД не вернул результатов"

        return query_result


db_user_query = UserClient()
db_post_query = PostClient()
db_comment_query = CommentClient()
