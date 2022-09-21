import datetime

import factory.fuzzy
from core.factories.car import CarFactory
from factory.django import DjangoModelFactory
from provider.factories.provider import ProviderFactory
from provider.models import ProviderHistory
from shop.factories.shop import ShopFactory


class ProviderHistoryFactory(DjangoModelFactory):
    provider = factory.SubFactory(ProviderFactory)
    car = factory.SubFactory(CarFactory)
    shop = factory.SubFactory(ShopFactory)
    purchase_time = factory.LazyFunction(datetime.datetime.now)
    price = "10.00"

    class Meta:
        model = ProviderHistory
