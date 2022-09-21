from django.db.models import Count, Sum

from shop.models import ShopHistory


def get_own_cars(client_id=None):
    return ShopHistory.objects.filter(client__id=client_id).values("car").annotate(car_count=Count("car"))


def get_costs(client_id=None):
    return ShopHistory.objects.filter(client__id=client_id).aggregate(total_costs=Sum("price"))
