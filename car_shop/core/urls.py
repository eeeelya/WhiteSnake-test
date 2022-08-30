from django.urls import include, path
from rest_framework import routers

from core.views import CarViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r"user", UserViewSet, basename="core_user")
router.register(r"cars", CarViewSet, basename="core_cars")

urlpatterns = [
    path("core/", include(router.urls)),
]
