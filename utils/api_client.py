import requests
from requests.auth import HTTPBasicAuth

from config.api_config import ADMIN_CREDS, BASE_URL


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(*ADMIN_CREDS)

    def post(self, endpoint, json=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=json, auth=self.auth)
        return response

    def delete(self, endpoint, json=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, json=json, auth=self.auth)  # , "force": "true"
        return response


api = ApiClient(BASE_URL)
