import factory
from core.factories.user import UserFactory
from factory.django import DjangoModelFactory
from provider.models import Provider


class ProviderFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory, user_type=2)
    name = factory.Sequence(lambda n: "test-provider-%d" % n)
    foundation_year = 2000
    total_clients = 0
    balance = "200.00"
    phone_number = factory.Sequence(lambda n: "+123456789%d" % n)
    location = "BY"
    is_active = True

    class Meta:
        model = Provider
