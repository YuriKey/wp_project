from faker import Faker

fake = Faker()


class UsersData:

    @staticmethod
    def create_minimal_user_data():
        """
        Создает минимальный набор данных для пользователя.
        """
        username = fake.user_name()
        user_data = {
            "username": f"{username}",
            "email": f"{username}@{fake.domain_name()}",
            "password": f"{fake.password()}"
        }
        return user_data

    @staticmethod
    def create_full_user_data():
        username = fake.user_name()
        user_data = {
            "username": f"{username}",
            "login": f"{username}.{fake.last_name()}",
            "user_nicename": f"{fake.first_name()}",
            "email": f"{username}@{fake.domain_name()}",
            "password": f"{fake.password()}"
        }
        return user_data

    @staticmethod
    def create_user_data_without_username():
        username = fake.user_name()
        user_data = {
            "name": f"{username}",
            "last_name": f"{fake.last_name()}",
            "email": f"{username}@{fake.domain_name()}",
            "password": f"{fake.password()}"
        }
        return user_data
