import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.factories.user import UserFactory
from core.token import get_token
from provider.factories.provider import ProviderFactory
from provider.factories.provider_sale import ProviderSaleFactory


class ProviderSaleViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.endpoint = "/api/v1/provider/sales/"
        self.api_client = APIClient()

    def test_create(self):
        user = UserFactory(user_type=2)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        provider = ProviderFactory(user=user)

        provider_sale = ProviderSaleFactory(provider=provider)

        data = {
            "name": provider_sale.name,
            "shop": provider_sale.shop.id,
            "start_datetime": provider_sale.start_datetime,
            "end_datetime": provider_sale.end_datetime,
            "discount_amount": provider_sale.discount_amount,
            "description": provider_sale.description,
        }
        response = self.api_client.post(self.endpoint, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        user = UserFactory(user_type=2)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        provider = ProviderFactory(user=user)
        ProviderSaleFactory(provider=provider)

        response = self.api_client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_retrieve(self):
        user = UserFactory(user_type=2)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        provider = ProviderFactory(user=user)
        provider_sale = ProviderSaleFactory(provider=provider)

        response = self.api_client.get(f"{self.endpoint}{provider_sale.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 6)

    def test_update(self):
        user = UserFactory(user_type=2)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        provider = ProviderFactory(user=user)

        provider_sale = ProviderSaleFactory(provider=provider)
        new_provider_sale = ProviderSaleFactory(provider=provider)

        data = {
            "name": new_provider_sale.name,
            "shop": new_provider_sale.shop.id,
            "start_datetime": new_provider_sale.start_datetime,
            "end_datetime": new_provider_sale.end_datetime,
            "discount_amount": new_provider_sale.discount_amount,
            "description": new_provider_sale.description,
        }

        response = self.api_client.put(f"{self.endpoint}{provider_sale.id}/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        user = UserFactory(user_type=2)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        provider = ProviderFactory(user=user)

        provider_sale = ProviderSaleFactory(provider=provider)
        new_provider_sale = ProviderSaleFactory(provider=provider)

        data = {
            "start_datetime": new_provider_sale.start_datetime,
            "end_datetime": new_provider_sale.end_datetime,
            "discount_amount": new_provider_sale.discount_amount,
        }

        response = self.api_client.patch(f"{self.endpoint}{provider_sale.id}/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        user = UserFactory(user_type=2)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        provider = ProviderFactory(user=user)
        provider_sale = ProviderSaleFactory(provider=provider)

        response = self.api_client.delete(f"{self.endpoint}{provider_sale.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
