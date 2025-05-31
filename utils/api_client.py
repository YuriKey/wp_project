import requests
from requests.auth import HTTPBasicAuth

from config.api_config import ADMIN_CREDS, Endpoints as ep


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(*ADMIN_CREDS)

    def _send_request(self, method, endpoint, json=None, expected_status=200):
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, json=json, auth=self.auth)
        assert response.status_code == expected_status, (
            f"Ожидался статус {expected_status}, получен {response.status_code}: {response.text}"
        )
        return response

    def post(self, endpoint, json=None, expected_status=201):
        return self._send_request("POST", endpoint, json=json, expected_status=expected_status)

    def delete(self, endpoint, json=None, expected_status=200):
        return self._send_request("DELETE", endpoint, json=json, expected_status=expected_status)


class UsersApi(ApiClient):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.endpoint = ep.USERS_ENDPOINT

    def create_user(self, data):
        response = self.post(
            self.endpoint
            , json=data
            , expected_status=201)
        return response

    def update_user(self, user_id, data):
        self.post(
            f"{self.endpoint}/{user_id}"
            , json=data
            , expected_status=200)

    def delete_user(self, user_id):
        self.delete(
            f"{self.endpoint}/{user_id}"
            , json={"reassign": 1, "force": True}
            , expected_status=200)


class PostsApi(ApiClient):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.endpoint = ep.POSTS_ENDPOINT

    def create_post(self, data):
        response = self.post(
            self.endpoint
            , json=data
            , expected_status=201)
        return response

    def update_post(self, post_id, data):
        self.post(
            f"{self.endpoint}/{post_id}"
            , json=data
            , expected_status=200)

    def delete_post(self, post_id):
        self.delete(
            f"{self.endpoint}/{post_id}"
            , expected_status=200)


class CommentsApi(ApiClient):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.endpoint = ep.COMMENTS_ENDPOINT

    def create_comment(self, data):
        response = self.post(
            self.endpoint
            , json=data
            , expected_status=201)
        return response

    def update_comment(self, comment_id, data):
        self.post(
            f"{self.endpoint}/{comment_id}"
            , json=data
            , expected_status=200)

    def delete_comment(self, comment_id, data=None):
        self.delete(
            f"{self.endpoint}/{comment_id}"
            , json=data
            , expected_status=200)
