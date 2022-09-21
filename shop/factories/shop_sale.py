import datetime

import factory.fuzzy
from core.factories.car import CarFactory
from factory.django import DjangoModelFactory
from shop.factories.shop import ShopFactory
from shop.models import ShopSale


class ShopSaleFactory(DjangoModelFactory):
    car = factory.SubFactory(CarFactory)
    shop = factory.SubFactory(ShopFactory)
    name = factory.Sequence(lambda n: "test-sale-%d" % n)
    start_datetime = factory.LazyFunction(datetime.datetime.now)
    end_datetime = factory.LazyFunction(datetime.datetime.now)
    discount_amount = "5"
    description = "Test description"

    class Meta:
        model = ShopSale
