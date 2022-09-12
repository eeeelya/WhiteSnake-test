import django_filters as filters
from client.models import Client


class ClientFilter(filters.FilterSet):
    age__gte = filters.NumberFilter(field_name="age", lookup_expr="gte")
    age__lte = filters.NumberFilter(field_name="age", lookup_expr="lte")
    sex = filters.ChoiceFilter(choices=Client.SEX_CHOICES)
    balance__gte = filters.NumberFilter(field_name="balance", lookup_expr="gte")
    balance__lte = filters.NumberFilter(field_name="balance", lookup_expr="lte")

    class Meta:
        model = Client
        fields = ["age__gte", "age__lte", "sex", "balance__gte", "balance__gte"]
