import os
from dotenv import load_dotenv

load_dotenv()


DB_CONFIG = {
    "server": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}

# Строка подключения к базе данных
CONNECT_STRING = (
    f"DRIVER={{MySQL ODBC 8.0 Unicode Driver}};"
    f"SERVER={DB_CONFIG['server']};"
    f"DATABASE={DB_CONFIG['database']};"
    f"UID={DB_CONFIG['user']};"
    f"PWD={DB_CONFIG['password']};"
    f"PORT={DB_CONFIG['port']}"
)
