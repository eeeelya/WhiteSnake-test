import factory.fuzzy
from client.models import Client, get_default_specification
from core.factories.user import UserFactory
from factory.django import DjangoModelFactory


class ClientFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory, user_type=1)
    age = factory.Faker("pyint", min_value=0, max_value=100)
    sex = factory.fuzzy.FuzzyChoice(choices=Client.Sex.choices, getter=lambda c: c[0])
    balance = "200.00"
    specification = get_default_specification()
    phone_number = factory.Sequence(lambda n: "+123456789%d" % n)
    location = "BY"
    is_active = True

    class Meta:
        model = Client
