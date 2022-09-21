from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from provider.filters import ProviderFilter
from provider.models import Provider, ProviderCar, ProviderHistory, ProviderSale
from provider.permissions import IsProviderOrSuperUser, UpdatePermission
from provider.serializers import (
    ProviderCarSerializer,
    ProviderHistorySerializer,
    ProviderSaleSerializer,
    ProviderSerializer,
)
from provider.statistics import get_sold_cars, get_unsold_cars


class ProviderViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, UpdatePermission)
    serializer_class = ProviderSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ProviderFilter

    def get_queryset(self):
        return Provider.objects.filter(is_active=True)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        instance = self.get_object()

        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
    def cars(self, request, pk=None):
        cars = ProviderCar.objects.filter(provider=pk)

        serializer = ProviderCarSerializer(cars, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        history = ProviderHistory.objects.filter(provider=pk)

        serializer = ProviderHistorySerializer(history, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def sold_cars(self, request, pk=None):
        sold_cars = get_sold_cars(pk)

        return Response(sold_cars, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def unsold_cars(self, request, pk=None):
        unsold_cars = get_unsold_cars(pk)

        return Response(unsold_cars, status=status.HTTP_200_OK)


class ProviderSaleViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsProviderOrSuperUser)
    serializer_class = ProviderSaleSerializer

    def get_queryset(self):
        return ProviderSale.objects.filter(provider__user=self.request.user.pk, is_active=True)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        sales = self.get_queryset()
        serializer = self.get_serializer(sales, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def delete(self, request, pk=None):
        instance = self.get_object()

        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
