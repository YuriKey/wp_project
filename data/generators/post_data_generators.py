from faker import Faker

fake = Faker()


class PostData:

    def generate_minimal_post_data(self):
        post_data = {
            "title": fake.text(max_nb_chars=60),
        }

        return post_data

    def generate_full_post_data(self):
        post_data = {
            "post_title": fake.text(max_nb_chars=60),
            "post_date": fake.date_time(),
            "post_date_gmt": fake.date_time(),
            "post_modified": fake.date_time(),
            "post_modified_gmt": fake.date_time(),
            "post_content": fake.text(max_nb_chars=1000),
            "post_excerpt": fake.text(max_nb_chars=100),
            "to_ping": fake.url(),
            "pinged": fake.url(),
            "post_content_filtered": fake.text(max_nb_chars=1000)
        }

        return post_data


generated_post_data = PostData()
