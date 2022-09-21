import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.factories.user import UserFactory
from core.token import get_token


class UserInfoViewSetTest(APITestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.endpoint = "/api/v1/core/user-info/"
        cls.users = UserFactory.create_batch(3)

    @staticmethod
    def authenticate_client(user_type=1):
        user = UserFactory(user_type=user_type)
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(user))

        return api_client

    def test_list(self):
        api_client = self.authenticate_client()
        response = api_client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        api_client = self.authenticate_client(user_type=4)
        response = api_client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        api_client = self.authenticate_client()

        response = api_client.get(f"{self.endpoint}{self.users[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 5)

    def test_delete(self):
        api_client = self.authenticate_client()

        response = api_client.delete(f"{self.endpoint}{self.users[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
