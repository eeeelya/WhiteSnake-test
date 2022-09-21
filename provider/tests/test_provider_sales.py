import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.factories.user import UserFactory
from core.token import get_token
from provider.factories.provider import ProviderFactory
from provider.factories.provider_sale import ProviderSaleFactory


class ProviderSaleViewSetTest(APITestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.endpoint = "/api/v1/provider/sales/"

        user = UserFactory(user_type=2)
        provider = ProviderFactory(user=user)
        provider_sale = ProviderSaleFactory(provider=provider)

        cls.data = {
            "name": provider_sale.name,
            "shop": provider_sale.shop.id,
            "start_datetime": provider_sale.start_datetime,
            "end_datetime": provider_sale.end_datetime,
            "discount_amount": provider_sale.discount_amount,
            "description": provider_sale.description,
        }

        cls.user = user
        cls.provider = provider
        cls.provider_sale = provider_sale
        cls.provider_sales = ProviderSaleFactory.create_batch(2)

    def authenticate_client(self):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(self.user))

        return api_client

    def test_create(self):
        api_client = self.authenticate_client()

        response = api_client.post(self.endpoint, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        api_client = self.authenticate_client()

        response = api_client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_retrieve(self):
        api_client = self.authenticate_client()

        response = api_client.get(f"{self.endpoint}{self.provider_sale.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 6)

    def test_update(self):
        api_client = self.authenticate_client()

        provider_sale = ProviderSaleFactory.build(provider=self.provider)
        self.data["name"] = provider_sale.name

        response = api_client.put(f"{self.endpoint}{self.provider_sale.id}/", self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        api_client = self.authenticate_client()

        new_provider_sale = ProviderSaleFactory(provider=self.provider)
        new_data = {"start_datetime": new_provider_sale.start_datetime}

        response = api_client.patch(f"{self.endpoint}{self.provider_sale.id}/", new_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        api_client = self.authenticate_client()

        response = api_client.delete(f"{self.endpoint}{self.provider_sale.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
