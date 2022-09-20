import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.factories.car import CarFactory


class CarViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.endpoint = "/api/v1/core/cars/"
        self.api_client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.users = CarFactory.create_batch(3)

    def test_create_car(self):
        data = {
            "name": "test-car",
            "manufacture_year": 2000,
            "type": "Sed",
            "fuel": "P",
            "color": "test-color",
            "description": "Test",
        }
        response = self.api_client.post(self.endpoint, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), data)

    def test_list_car(self):
        response = self.api_client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 3)

    def test_retrieve_car(self):
        response = self.api_client.get(f"{self.endpoint}{self.users[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 6)

    def test_update_car(self):
        data = {
            "name": "new-test-car",
            "manufacture_year": 2000,
            "type": "Sed",
            "fuel": "P",
            "color": "test-color",
            "description": "Test",
        }
        response = self.api_client.put(f"{self.endpoint}{self.users[0].id}/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    def test_delete_car(self):
        response = self.api_client.delete(f"{self.endpoint}{self.users[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
