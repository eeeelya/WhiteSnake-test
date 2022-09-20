from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from provider.models import ProviderHistory
from provider.serializers import ProviderHistorySerializer
from shop.filters import ShopFilter
from shop.models import Shop, ShopCar, ShopHistory, ShopSale
from shop.permissions import GetPermission, UpdatePermission
from shop.serializers import ShopCarSerializer, ShopHistorySerializer, ShopSaleSerializer, ShopSerializer
from shop.statistics import get_cars_price, get_clients_popular_countries, get_costs, get_proceeds


class ShopViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, UpdatePermission)
    serializer_class = ShopSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ShopFilter

    def get_queryset(self):
        return Shop.objects.filter(is_active=True)

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

        if not instance.is_active:
            return Response({"detail": "instance is inactive"}, status=status.HTTP_400_BAD_REQUEST)

        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        if "balance" in request.data:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            self.partial_update(request, pk)

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def cars(self, request, pk=None):
        cars = ShopCar.objects.filter(shop=pk)

        serializer = ShopCarSerializer(cars, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "shop doesn't have cars"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, url_path="clients-history", methods=["get"])
    def clients_history(self, request, pk=None):
        history = ShopHistory.objects.filter(shop=pk)

        serializer = ShopHistorySerializer(history, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "shop doesn't have history with clients"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, url_path="providers-history", methods=["get"])
    def providers_history(self, request, pk=None):
        history = ProviderHistory.objects.filter(shop=pk)

        serializer = ProviderHistorySerializer(history, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "shop doesn't have history with providers"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, url_path="cars-price", methods=["get"])
    def cars_price(self, request, pk=None):
        cars_price = get_cars_price(pk)

        return Response(cars_price, status=status.HTTP_200_OK)

    @action(detail=True, url_path="cash-account", methods=["get"])
    def cash_account(self, request, pk=None):
        data = {}

        costs = get_costs(pk)
        data["costs"] = costs["total_costs"]
        proceeds = get_proceeds(pk)
        data["proceeds"] = proceeds["total_proceeds"]
        data["profit"] = proceeds["total_proceeds"] - costs["total_costs"]

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, url_path="popular-countries", methods=["get"])
    def popular_countries(self, request, pk=None):
        countries = get_clients_popular_countries(pk)

        return Response(countries, status=status.HTTP_200_OK)


class ShopSaleViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, GetPermission)
    serializer_class = ShopSaleSerializer

    def get_queryset(self):
        return ShopSale.objects.filter(shop__user=self.request.user.pk, is_active=True)

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
