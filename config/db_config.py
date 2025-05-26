# config/config.py

# Конфигурация MySQL
DB_CONFIG = {
    "server": "localhost",
    "database": "wordpress",
    "user": "wordpress",
    "password": "wordpress",
    "port": "3306"
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
