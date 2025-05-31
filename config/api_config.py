import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ADMIN_CREDS = (os.getenv("ADMIN_LOGIN"), os.getenv("ADMIN_PASSWORD"))


class Endpoints:
    USERS_ENDPOINT = "/wp/v2/users"
    POSTS_ENDPOINT = "/wp/v2/posts"
    COMMENTS_ENDPOINT = "/wp/v2/comments"
