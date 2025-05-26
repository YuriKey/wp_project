import pyodbc


def test_drivers():
    print(pyodbc.drivers())


def test_odbc():
    try:
        conn = pyodbc.connect(
            "DRIVER={MySQL ODBC 8.0 Unicode Driver};"
            "SERVER=localhost;"
            "DATABASE=wordpress;"
            "UID=wordpress;"
            "PWD=wordpress;"
            "PORT=3306"
        )
        print("Успешное подключение!")
        conn.close()
    except Exception as e:
        print(f"Ошибка: {e}")
