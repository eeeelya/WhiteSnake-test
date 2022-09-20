import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.factories.user import UserFactory
from core.token import get_token
from shop.factories.shop import ShopFactory
from shop.factories.shop_sale import ShopSaleFactory


class ShopSaleViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.endpoint = "/api/v1/shop/sales/"
        self.api_client = APIClient()

    def test_create(self):
        user = UserFactory(user_type=3)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        shop = ShopFactory(user=user)
        shop_sale = ShopSaleFactory(shop=shop)

        data = {
            "name": shop_sale.name,
            "car": shop_sale.car.id,
            "start_datetime": shop_sale.start_datetime,
            "end_datetime": shop_sale.end_datetime,
            "discount_amount": shop_sale.discount_amount,
            "description": shop_sale.description,
        }
        response = self.api_client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        user = UserFactory(user_type=3)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        shop = ShopFactory(user=user)
        ShopSaleFactory(shop=shop)

        response = self.api_client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_retrieve(self):
        user = UserFactory(user_type=3)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        shop = ShopFactory(user=user)
        shop_sale = ShopSaleFactory(shop=shop)

        response = self.api_client.get(f"{self.endpoint}{shop_sale.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 6)

    def test_update(self):
        user = UserFactory(user_type=3)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        shop = ShopFactory(user=user)
        shop_sale = ShopSaleFactory(shop=shop)
        new_shop_sale = ShopSaleFactory(shop=shop)

        data = {
            "name": new_shop_sale.name,
            "car": new_shop_sale.car.id,
            "start_datetime": new_shop_sale.start_datetime,
            "end_datetime": new_shop_sale.end_datetime,
            "discount_amount": new_shop_sale.discount_amount,
            "description": new_shop_sale.description,
        }

        response = self.api_client.put(f"{self.endpoint}{shop_sale.id}/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        user = UserFactory(user_type=3)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        shop = ShopFactory(user=user)
        shop_sale = ShopSaleFactory(shop=shop)
        new_shop_sale = ShopSaleFactory(shop=shop)

        data = {
            "start_datetime": new_shop_sale.start_datetime,
            "end_datetime": new_shop_sale.end_datetime,
            "discount_amount": new_shop_sale.discount_amount,
        }
        response = self.api_client.patch(f"{self.endpoint}{shop_sale.id}/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        user = UserFactory(user_type=3)
        self.api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        shop = ShopFactory(user=user)
        shop_sale = ShopSaleFactory(shop=shop)

        response = self.api_client.delete(f"{self.endpoint}{shop_sale.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
