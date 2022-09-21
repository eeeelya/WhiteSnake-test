from django.urls import include, path
from rest_framework import routers

from client.views import ClientViewSet

router = routers.DefaultRouter()
router.register(r"", ClientViewSet, basename="client")

urlpatterns = [
    path("client/", include(router.urls)),
]
