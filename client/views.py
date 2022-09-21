from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from client.filters import ClientFilter
from client.models import Client
from client.permissions import UpdatePermission
from client.serializers import ClientSerializer
from client.statistics import get_costs, get_own_cars
from django_filters.rest_framework import DjangoFilterBackend
from shop.models import ShopHistory
from shop.serializers import ShopHistorySerializer


class ClientViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated, UpdatePermission)
    filter_backends = (DjangoFilterBackend,)
    filter_class = ClientFilter

    def get_queryset(self):
        return Client.objects.filter(is_active=True)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        instance = self.get_object()

        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        cars = ShopHistory.objects.filter(client__user=request.user)

        serializer = ShopHistorySerializer(cars, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="cars")
    def own_cars(self, request, pk=None):
        cars = get_own_cars(pk)

        return Response(cars, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def costs(self, request, pk=None):
        cars = get_costs(pk)

        return Response(cars, status=status.HTTP_200_OK)
