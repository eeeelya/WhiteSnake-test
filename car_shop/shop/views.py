from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from provider.models import ProviderHistory
from provider.serializers import ProviderHistorySerializer
from shop.models import Shop, ShopCar, ShopHistory, ShopSale
from shop.permissions import IsAdminOrSuperUserForUpdate, IsShopOrSuperUser
from shop.serializers import ShopCarSerializer, ShopHistorySerializer, ShopSaleSerializer, ShopSerializer


class ShopViewSet(viewsets.GenericViewSet):
    queryset = Shop.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrSuperUserForUpdate)
    serializer_class = ShopSerializer

    def get_queryset(self):
        return Shop.objects.filter(is_active=True)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No active instances"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        instance = self.get_object()

        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        instance = self.get_object()

        if not instance.is_active:
            return Response({"detail": "instance is inactive"}, status=status.HTTP_400_BAD_REQUEST)

        instance.is_active = False
        instance.save()

        return Response({"detail": "instance moved to inactive"}, status=status.HTTP_200_OK)

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
        cars = ShopCar.objects.filter(provider=pk)

        serializer = ShopCarSerializer(cars, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "shop doesn't have cars"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["get"])
    def clients_history(self, request, pk=None):
        history = ShopHistory.objects.filter(provider=pk)

        serializer = ShopHistorySerializer(history, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "shop doesn't have history with clients"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["get"])
    def providers_history(self, request, pk=None):
        history = ProviderHistory.objects.filter(provider=pk)

        serializer = ProviderHistorySerializer(history, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "shop doesn't have history with providers"}, status=status.HTTP_404_NOT_FOUND)


class ShopSaleViewSet(viewsets.GenericViewSet):
    queryset = ShopSale.objects.all()
    permission_classes = (IsAuthenticated, IsShopOrSuperUser)
    serializer_class = ShopSaleSerializer

    def get_queryset(self):
        return ShopSale.objects.filter(shop__user=self.request.user.pk, is_active=True)

    def list(self, request):
        sales = self.get_queryset()
        serializer = self.get_serializer(sales, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        instance = self.get_object()

        instance.is_active = False
        instance.save()

        return Response({"detail": "instance moved to inactive"}, status=status.HTTP_200_OK)

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
