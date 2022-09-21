import json

import pytest
from client.factories.client import ClientFactory
from core.factories.user import UserFactory
from core.token import get_token
from shop.factories.shop_history import ShopHistoryFactory


class TestClientViewSet:
    pytestmark = pytest.mark.django_db
    endpoint = "/api/v1/client/"

    def test_list(self, api_client):
        clients = ClientFactory.create_batch(3)

        api_client.credentials(HTTP_AUTHORIZATION=get_token(clients[0].user))

        response = api_client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client):
        user = UserFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(user))

        client = ClientFactory.build()

        data = {
            "age": client.age,
            "sex": client.sex,
            "balance": client.balance,
            "specification": client.specification,
            "phone_number": str(client.phone_number),
            "location": str(client.location),
        }

        response = api_client.post(self.endpoint, data, format="json")

        assert response.status_code == 201
        assert json.loads(response.content) == data

    def test_retrieve(self, api_client):
        client = ClientFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(client.user))

        data = {
            "age": client.age,
            "sex": client.sex,
            "balance": client.balance,
            "specification": client.specification,
            "phone_number": str(client.phone_number),
            "location": str(client.location),
        }

        response = api_client.get(f"{self.endpoint}{client.id}/")

        assert response.status_code == 200
        assert json.loads(response.content) == data

    def test_update(self, rf, api_client):
        client = ClientFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(client.user))

        new_client = ClientFactory.build()

        new_data = {
            "age": new_client.age,
            "sex": new_client.sex,
            "balance": new_client.balance,
            "specification": new_client.specification,
            "phone_number": str(new_client.phone_number),
            "location": str(new_client.location),
        }

        response_for_client = api_client.put(f"{self.endpoint}{client.id}/", new_data, format="json")
        assert response_for_client.status_code == 403

        user = UserFactory(user_type=4)
        api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        response_for_admin = api_client.put(f"{self.endpoint}{client.id}/", new_data, format="json")

        assert response_for_admin.status_code == 200
        assert json.loads(response_for_admin.content) == new_data

    def test_partial_update(self, api_client):
        client = ClientFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(client.user))

        new_client = ClientFactory.build()

        data_with_balance = {"age": new_client.age, "sex": new_client.sex, "balance": new_client.balance}

        response = api_client.patch(f"{self.endpoint}{client.id}/", data_with_balance, format="json")

        assert response.status_code == 403

        clear_data = {
            "age": new_client.age,
            "sex": new_client.sex,
        }

        response = api_client.patch(f"{self.endpoint}{client.id}/", clear_data, format="json")

        assert response.status_code == 200

    def test_delete(self, api_client):
        client = ClientFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(client.user))

        response = api_client.delete(f"{self.endpoint}{client.id}/")

        assert response.status_code == 204

    def test_history(self, api_client):
        client = ClientFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(client.user))

        ShopHistoryFactory.create_batch(3, client=client)

        response = api_client.get(f"{self.endpoint}{client.id}/history/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_own_cars(self, api_client):
        client = ClientFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(client.user))

        ShopHistoryFactory.create_batch(4, client=client)

        response = api_client.get(f"{self.endpoint}{client.id}/cars/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    def test_costs(self, api_client):
        client = ClientFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(client.user))

        price = 100
        ShopHistoryFactory.create_batch(2, client=client, price=price)

        response = api_client.get(f"{self.endpoint}{client.id}/costs/")

        data = json.loads(response.content)

        assert response.status_code == 200
        assert data["total_costs"] == price * 2
