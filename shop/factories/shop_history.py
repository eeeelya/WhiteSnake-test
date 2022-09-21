import datetime

import factory.fuzzy
from client.factories.client import ClientFactory
from core.factories.car import CarFactory
from factory.django import DjangoModelFactory
from shop.factories.shop import ShopFactory
from shop.models import ShopHistory


class ShopHistoryFactory(DjangoModelFactory):
    client = factory.SubFactory(ClientFactory)
    car = factory.SubFactory(CarFactory)
    shop = factory.SubFactory(ShopFactory)
    purchase_time = factory.LazyFunction(datetime.datetime.now)
    price = "10.00"

    class Meta:
        model = ShopHistory
