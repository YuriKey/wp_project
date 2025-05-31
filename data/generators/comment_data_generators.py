from faker import Faker

fake = Faker()


class CommentData:
    @staticmethod
    def generate_comment_data(post_id):
        data_comment = {
            "post": post_id,
            "content": fake.text(max_nb_chars=150)
        }
        return data_comment

    @staticmethod
    def generate_comment_data_author():
        data = {
            "content": f"{fake.text(max_nb_chars=1000)}",
            "author_name": f"{fake.last_name()}"
        }
        return data
