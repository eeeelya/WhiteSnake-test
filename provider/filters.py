import django_filters as filters
from provider.models import Provider


class ProviderFilter(filters.FilterSet):
    foundation_year__gte = filters.NumberFilter(field_name="foundation_year", lookup_expr="gte")
    foundation_year__lte = filters.NumberFilter(field_name="foundation_year", lookup_expr="lte")
    balance__gte = filters.NumberFilter(field_name="balance", lookup_expr="gte")
    balance__lte = filters.NumberFilter(field_name="balance", lookup_expr="lte")

    class Meta:
        model = Provider
        fields = ["foundation_year", "balance"]
