import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.factories.user import UserFactory
from core.token import get_token


class UserInfoViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.endpoint = "/api/v1/core/user-info/"
        self.api_client = APIClient()

    def test_list(self):
        user = UserFactory(user_type=1)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))

        UserFactory.create_batch(3)

        response = self.api_client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve(self):
        user = UserFactory()
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))

        response = self.api_client.get(f"{self.endpoint}{user.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 5)

    def test_delete(self):
        user = UserFactory()
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))

        response = self.api_client.delete(f"{self.endpoint}{user.id}/")

        user_object = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_object["detail"], "instance moved to inactive")
