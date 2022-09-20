from django.urls import include, path
from rest_framework import routers

from core.views import CarViewSet, UserAuthViewSet, UserInfoViewSet

router = routers.DefaultRouter()
router.register(r"user-auth", UserAuthViewSet, basename="core_user-auth")
router.register(r"user-info", UserInfoViewSet, basename="core_user-info")
router.register(r"cars", CarViewSet, basename="core_cars")

urlpatterns = [
    path("core/", include(router.urls)),
]
