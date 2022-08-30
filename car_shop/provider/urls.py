from django.urls import include, path
from rest_framework import routers

from provider.views import ProviderSaleViewSet, ProviderViewSet

provider_router = routers.DefaultRouter()
provider_router.register(r"sales", ProviderSaleViewSet, basename="provider_sale")
provider_router.register(r"", ProviderViewSet, basename="provider")

urlpatterns = [
    path("provider/", include(provider_router.urls)),
]
