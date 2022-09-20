import datetime

import factory.fuzzy
from factory.django import DjangoModelFactory
from provider.factories.provider import ProviderFactory
from provider.models import ProviderSale
from shop.factories.shop import ShopFactory


class ProviderSaleFactory(DjangoModelFactory):
    provider = factory.SubFactory(ProviderFactory)
    shop = factory.SubFactory(ShopFactory)
    name = factory.Sequence(lambda n: "test-sale-%d" % n)
    start_datetime = factory.LazyFunction(datetime.datetime.now)
    end_datetime = factory.LazyFunction(datetime.datetime.now)
    discount_amount = "5"
    description = "Test description"

    class Meta:
        model = ProviderSale
