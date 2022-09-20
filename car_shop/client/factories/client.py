import factory.fuzzy
from client.models import Client, get_default_specification
from core.factories.user import UserFactory
from factory.django import DjangoModelFactory

SEX_CHOICE_IDS = [x[0] for x in Client.SEX_CHOICES]


class ClientFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory, user_type=1)
    age = 20
    sex = factory.fuzzy.FuzzyChoice(SEX_CHOICE_IDS)
    balance = "200.00"
    specification = get_default_specification()
    phone_number = factory.Sequence(lambda n: "123-456-789%d" % n)
    location = "BY"
    is_active = True

    class Meta:
        model = Client
