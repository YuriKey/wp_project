# Настройки (URL, DB, пользователи)
import pymysql
from pymysql.cursors import DictCursor


API_URL = "http://localhost:8000/wp-json/wp/v2"

DB_CONFIG = {
    "host": "localhost",  # Или "db-1", если обращение внутри Docker-сети
    "user": "wordpress",  # Стандартный пользователь WordPress
    "password": "wordpress",  # Пароль из docker-compose.yml
    "database": "wordpress",
    "port": 3306,  # Порт MySQL
    "cursorclass": pymysql.cursors.DictCursor,
}
ADMIN_CREDS = ("yuri.krenev", "123-Test")  # Логин/пароль для Basic Auth
