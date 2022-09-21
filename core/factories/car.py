import datetime

import factory.fuzzy
from core.models import Car
from factory.django import DjangoModelFactory


class CarFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "test-car-%d" % n)
    manufacture_year = factory.Faker("pyint", min_value=1900, max_value=datetime.datetime.now().year)
    fuel = factory.fuzzy.FuzzyChoice(choices=Car.FuelType.choices, getter=lambda c: c[0])
    type = factory.fuzzy.FuzzyChoice(choices=Car.CarType.choices, getter=lambda c: c[0])
    color = factory.Faker("color")
    description = "Test description"

    class Meta:
        model = Car
