# Обёртка для requests
import requests
from requests.auth import HTTPBasicAuth


class ApiClient:
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(*auth)

    def post(self, endpoint, json):
        return requests.post(f"{self.base_url}{endpoint}", json=json, auth=self.auth)


    # Добавить методы get, put, delete...
