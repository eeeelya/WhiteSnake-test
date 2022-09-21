import json

import pytest
from core.factories.user import UserFactory
from core.token import get_token
from provider.factories.provider_history import ProviderHistoryFactory
from shop.factories.shop import ShopFactory
from shop.factories.shop_car import ShopCarFactory
from shop.factories.shop_history import ShopHistoryFactory


class TestShopViewSet:
    pytestmark = pytest.mark.django_db
    endpoint = "/api/v1/shop/"

    def test_list(self, api_client):
        shops = ShopFactory.create_batch(3)
        api_client.credentials(HTTP_AUTHORIZATION=get_token(shops[0].user))

        response = api_client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client):
        user = UserFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(user))

        shop = ShopFactory.build()

        data = {
            "name": shop.name,
            "specification": shop.specification,
            "balance": shop.balance,
            "phone_number": str(shop.phone_number),
            "location": str(shop.location),
        }

        response = api_client.post(self.endpoint, data, format="json")

        assert response.status_code == 201
        assert json.loads(response.content) == data

    def test_retrieve(self, api_client):
        shop = ShopFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(shop.user))

        data = {
            "name": shop.name,
            "specification": shop.specification,
            "balance": shop.balance,
            "phone_number": str(shop.phone_number),
            "location": str(shop.location),
        }

        response = api_client.get(f"{self.endpoint}{shop.id}/")

        assert response.status_code == 200
        assert json.loads(response.content) == data

    def test_update(self, rf, api_client):
        shop = ShopFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(shop.user))

        new_shop = ShopFactory.build()

        new_data = {
            "name": new_shop.name,
            "specification": new_shop.specification,
            "balance": new_shop.balance,
            "phone_number": str(new_shop.phone_number),
            "location": str(new_shop.location),
        }

        response_for_provider = api_client.put(f"{self.endpoint}{shop.id}/", new_data, format="json")
        assert response_for_provider.status_code == 403

        admin = UserFactory(user_type=4)
        api_client.credentials(HTTP_AUTHORIZATION=get_token(admin))
        response_for_admin = api_client.put(f"{self.endpoint}{shop.id}/", new_data, format="json")

        assert response_for_admin.status_code == 200
        assert json.loads(response_for_admin.content) == new_data

    def test_partial_update(self, api_client):
        shop = ShopFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(shop.user))

        new_shop = ShopFactory.build()

        data_with_balance = {
            "specification": new_shop.specification,
            "balance": new_shop.balance,
        }

        response = api_client.patch(f"{self.endpoint}{shop.id}/", data_with_balance, format="json")

        assert response.status_code == 403

        clear_data = {
            "specification": new_shop.specification,
        }

        response = api_client.patch(f"{self.endpoint}{shop.id}/", clear_data, format="json")

        assert response.status_code == 200

    def test_delete(self, api_client):
        shop = ShopFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(shop.user))

        response = api_client.delete(f"{self.endpoint}{shop.id}/")

        assert response.status_code == 204

    def test_cars(self, api_client):
        shop = ShopFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(shop.user))

        ShopCarFactory.create_batch(2, shop=shop)

        response = api_client.get(f"{self.endpoint}{shop.id}/cars/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2

    def test_clients_history(self, api_client):
        shop = ShopFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(shop.user))

        ShopHistoryFactory.create_batch(3, shop=shop)

        response = api_client.get(f"{self.endpoint}{shop.id}/clients-history/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_providers_history(self, api_client):
        shop = ShopFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(shop.user))

        ProviderHistoryFactory.create_batch(3, shop=shop)

        response = api_client.get(f"{self.endpoint}{shop.id}/providers-history/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_cars_price(self, api_client):
        shop = ShopFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(shop.user))

        price = 100
        ShopCarFactory.create_batch(3, shop=shop, price=price)

        response = api_client.get(f"{self.endpoint}{shop.id}/cars-price/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_cash_account(self, api_client):
        shop = ShopFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(shop.user))

        provider_price = 100
        shop_price = 120

        ShopHistoryFactory.create_batch(3, shop=shop, price=shop_price)
        ProviderHistoryFactory.create_batch(3, shop=shop, price=provider_price)

        response = api_client.get(f"{self.endpoint}{shop.id}/cash-account/")

        cash = json.loads(response.content)

        assert response.status_code == 200
        assert cash["profit"] > 0

    def test_popular_countries(self, api_client):
        shop = ShopFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(shop.user))

        ShopHistoryFactory.create_batch(3, shop=shop)
        response = api_client.get(f"{self.endpoint}{shop.id}/popular-countries/")

        countries = json.loads(response.content)

        assert response.status_code == 200
        assert len(countries) == 1
