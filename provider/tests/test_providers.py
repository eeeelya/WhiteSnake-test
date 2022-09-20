import json

import pytest
from core.factories.user import UserFactory
from core.token import get_token
from provider.factories.provider import ProviderFactory
from provider.factories.provider_car import ProviderCarFactory
from provider.factories.provider_history import ProviderHistoryFactory


class TestProviderViewSet:
    pytestmark = pytest.mark.django_db
    endpoint = "/api/v1/provider/"

    def test_list(self, api_client):
        providers = ProviderFactory.create_batch(3)

        api_client.credentials(HTTP_AUTHORIZATION=get_token(providers[0].user))

        response = api_client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client):
        user = UserFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(user))

        provider = ProviderFactory.build()
        data = {
            "name": provider.name,
            "foundation_year": provider.foundation_year,
            "total_clients": provider.total_clients,
            "balance": provider.balance,
            "phone_number": str(provider.phone_number),
            "location": str(provider.location),
        }

        response = api_client.post(self.endpoint, data, format="json")

        assert response.status_code == 201
        assert json.loads(response.content) == data

    def test_retrieve(self, api_client):
        provider = ProviderFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(provider.user))

        data = {
            "name": provider.name,
            "foundation_year": provider.foundation_year,
            "total_clients": provider.total_clients,
            "balance": provider.balance,
            "phone_number": str(provider.phone_number),
            "location": str(provider.location),
        }

        response = api_client.get(f"{self.endpoint}{provider.id}/")

        assert response.status_code == 200
        assert json.loads(response.content) == data

    def test_update(self, rf, api_client):
        provider = ProviderFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(provider.user))

        new_provider = ProviderFactory.build()

        new_data = {
            "name": new_provider.name,
            "foundation_year": new_provider.foundation_year,
            "total_clients": new_provider.total_clients,
            "balance": new_provider.balance,
            "phone_number": str(new_provider.phone_number),
            "location": str(new_provider.location),
        }

        response_for_provider = api_client.put(f"{self.endpoint}{provider.id}/", new_data, format="json")
        assert response_for_provider.status_code == 403

        user = UserFactory(user_type=4)
        api_client.credentials(HTTP_AUTHORIZATION=get_token(user))
        response_for_admin = api_client.put(f"{self.endpoint}{provider.id}/", new_data, format="json")

        assert response_for_admin.status_code == 200
        assert json.loads(response_for_admin.content) == new_data

    def test_partial_update(self, api_client):
        provider = ProviderFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(provider.user))

        new_provider = ProviderFactory.build()

        data_with_balance = {
            "name": new_provider.name,
            "foundation_year": new_provider.foundation_year,
            "total_clients": new_provider.total_clients,
            "balance": new_provider.balance,
        }

        response = api_client.patch(f"{self.endpoint}{provider.id}/", data_with_balance, format="json")

        assert response.status_code == 403

        clear_data = {
            "name": new_provider.name,
            "foundation_year": new_provider.foundation_year,
            "total_clients": new_provider.total_clients,
        }

        response = api_client.patch(f"{self.endpoint}{provider.id}/", clear_data, format="json")

        assert response.status_code == 200

    def test_delete(self, api_client):
        provider = ProviderFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(provider.user))

        response = api_client.delete(f"{self.endpoint}{provider.id}/")

        assert response.status_code == 204

    def test_cars(self, api_client):
        provider = ProviderFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(provider.user))

        ProviderCarFactory.create_batch(3, provider=provider)

        response = api_client.get(f"{self.endpoint}{provider.id}/cars/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_history(self, api_client):
        provider = ProviderFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(provider.user))

        ProviderHistoryFactory.create_batch(3, provider=provider)

        response = api_client.get(f"{self.endpoint}{provider.id}/history/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_sold_cars(self, api_client):
        provider = ProviderFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(provider.user))

        ProviderHistoryFactory.create_batch(5, provider=provider)

        response = api_client.get(f"{self.endpoint}{provider.id}/sold_cars/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 5

    def test_unsold_cars(self, api_client):
        provider = ProviderFactory()
        api_client.credentials(HTTP_AUTHORIZATION=get_token(provider.user))

        ProviderCarFactory.create_batch(5, provider=provider)

        response = api_client.get(f"{self.endpoint}{provider.id}/unsold_cars/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 5
