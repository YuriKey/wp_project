from faker import Faker

fake = Faker()


class CommentData:

    def generate_comment_data(self, post_id):

        data_comment = {
            "post": post_id,
            "content": fake.text(max_nb_chars=150)
        }
        return data_comment


generated_comment_data = CommentData()
