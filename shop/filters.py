import django_filters as filters
from shop.models import Shop


class ShopFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name")
    balance__gte = filters.NumberFilter(field_name="balance", lookup_expr="gte")
    balance__lte = filters.NumberFilter(field_name="balance", lookup_expr="lte")

    class Meta:
        model = Shop
        fields = ["balance__gte", "balance__lte", "name"]
