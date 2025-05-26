import requests
from requests.auth import HTTPBasicAuth


class ApiClient:
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(*auth)

    def post(self, endpoint, json):
        return requests.post(f"{self.base_url}{endpoint}", json=json, auth=self.auth)

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params)
        return response

    def put(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, data=data, json=json)
        return response

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url)
        return response
