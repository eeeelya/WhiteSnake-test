import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.factories.car import CarFactory
from core.factories.user import UserFactory
from core.token import get_token


class CarViewSetTest(APITestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.endpoint = "/api/v1/core/cars/"
        cls.cars = CarFactory.create_batch(3)

        car_data = CarFactory.build()
        cls.data = {
            "name": car_data.name,
            "manufacture_year": car_data.manufacture_year,
            "type": car_data.type,
            "fuel": car_data.fuel,
            "color": car_data.color,
            "description": car_data.description,
        }

    @staticmethod
    def authenticate_client():
        user = UserFactory(user_type=2)
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(user))

        return api_client

    def test_create(self):
        api_client = self.authenticate_client()

        response = api_client.post(self.endpoint, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), self.data)

    def test_list(self):
        api_client = self.authenticate_client()

        response = api_client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 3)

    def test_retrieve(self):
        api_client = self.authenticate_client()

        response = api_client.get(f"{self.endpoint}{self.cars[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 6)

    def test_update(self):
        api_client = self.authenticate_client()

        new_car = CarFactory.build()
        self.data["name"] = new_car.name

        response = api_client.put(f"{self.endpoint}{self.cars[0].id}/", self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.data)

    def test_delete(self):
        api_client = self.authenticate_client()

        response = api_client.delete(f"{self.endpoint}{self.cars[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
