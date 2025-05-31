import pyodbc

from config.db_config import CONNECT_STRING
from data.models.user import UserDB


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

        query_result = UserDB.from_db_row(db_response[0])
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

        query_result = UserDB.from_db_row(db_response[0])

        return query_result

    @staticmethod
    def db_create_user(user_data):
        from faker import Faker
        fake = Faker()

        with DbClient() as dbc:
            dbc.execute("""INSERT INTO wp_users (
                            user_pass, 
                            user_email,
                            display_name, 
                            user_registered, 
                            user_login, 
                            user_nicename) 
                            VALUES (?, ?, ?, ?, ?, ?)""",
                        (user_data["password"],
                         user_data["email"],
                         user_data["username"],
                         fake.date_time(),
                         user_data["login"],
                         user_data["user_nicename"]
                         ))

            user_id = dbc.query("SELECT ID FROM wp_users WHERE user_login = ?", (user_data["login"],)),

            return user_id[0][0]["ID"]

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

    @staticmethod
    def db_create_post(post_data):
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

        return post_id[0]["ID"]


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
