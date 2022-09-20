import factory.fuzzy
from core.factories.car import CarFactory
from factory.django import DjangoModelFactory
from provider.factories.provider import ProviderFactory
from provider.models import ProviderCar


class ProviderCarFactory(DjangoModelFactory):
    provider = factory.SubFactory(ProviderFactory)
    car = factory.SubFactory(CarFactory)
    count = factory.Faker("pyint", min_value=0, max_value=1000)
    price = "10.00"

    class Meta:
        model = ProviderCar
