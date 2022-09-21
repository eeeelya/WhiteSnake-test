import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.factories.user import UserFactory
from core.token import get_token
from shop.factories.shop import ShopFactory
from shop.factories.shop_sale import ShopSaleFactory


class ShopSaleViewSetTest(APITestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.endpoint = "/api/v1/shop/sales/"

        user = UserFactory(user_type=3)
        shop = ShopFactory(user=user)
        shop_sale = ShopSaleFactory(shop=shop)

        cls.data = {
            "name": shop_sale.name,
            "car": shop_sale.car.id,
            "start_datetime": shop_sale.start_datetime,
            "end_datetime": shop_sale.end_datetime,
            "discount_amount": shop_sale.discount_amount,
            "description": shop_sale.description,
        }

        cls.user = user
        cls.shop = shop
        cls.shop_sale = shop_sale
        cls.provider_sales = ShopSaleFactory.create_batch(2)

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

        response = api_client.get(f"{self.endpoint}{self.shop_sale.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 6)

    def test_update(self):
        api_client = self.authenticate_client()

        new_shop_sale = ShopSaleFactory.build(shop=self.shop)
        self.data["name"] = new_shop_sale.name

        response = api_client.put(f"{self.endpoint}{self.shop_sale.id}/", self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        api_client = self.authenticate_client()

        new_shop_sale = ShopSaleFactory(shop=self.shop)
        new_data = {
            "start_datetime": new_shop_sale.start_datetime,
        }

        response = api_client.patch(f"{self.endpoint}{self.shop_sale.id}/", new_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        api_client = self.authenticate_client()

        response = api_client.delete(f"{self.endpoint}{self.shop_sale.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
