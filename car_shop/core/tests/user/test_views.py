import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.factories.user import UserFactory


class UserViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.endpoint = "/api/v1/core/user/"
        self.api_client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.users = UserFactory.create_batch(3)

    def test_list_user(self):
        response = self.api_client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 3)

    def test_retrieve_user(self):
        response = self.api_client.get(f"{self.endpoint}{self.users[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 5)

    def test_delete_user(self):
        response = self.api_client.delete(f"{self.endpoint}{self.users[0].id}/")

        user_object = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_object["detail"], "instance moved to inactive")
