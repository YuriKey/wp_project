import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ADMIN_CREDS = (os.getenv("ADMIN_LOGIN"), os.getenv("ADMIN_PASSWORD"))
