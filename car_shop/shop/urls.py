from django.urls import include, path
from rest_framework import routers

from .views import ShopSaleViewSet, ShopViewSet

router = routers.DefaultRouter()
router.register(r"sales", ShopSaleViewSet, basename="shop_sale")
router.register(r"", ShopViewSet, basename="shop")

urlpatterns = [
    path("shop/", include(router.urls)),
]
