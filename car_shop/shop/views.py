from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Shop, ShopCar, ShopHistory, ShopSale
from .serializers import ShopCarSerializer, ShopHistorySerializer, ShopSaleSerializer, ShopSerializer


class ShopViewSet(viewsets.GenericViewSet):
    queryset = Shop.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopSerializer

    def list(self, request):
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(
                {"detail": "No active instances"}, status=status.HTTP_204_NO_CONTENT
            )

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        if instance.is_active:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "instance is inactive"}, status=status.HTTP_204_NO_CONTENT
            )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        instance = self.get_object()

        instance.is_active = False
        instance.save()

        return Response(
            {"detail": "instance moved to inactive"},
            status=status.HTTP_205_RESET_CONTENT,
        )

    def update(self, request, pk=None):
        instance = self.get_object()
        if "balance" in request.data:
            if request.user.user_type == 4 or request.user.is_superuser:
                serializer = self.get_serializer(instance, data=request.data)
            else:
                raise exceptions.PermissionDenied()
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=True, url_path="cars", methods=["get"])
    def cars(self, request, pk=None):
        cars = ShopCar.objects.filter(provider=pk)

        serializer = ShopCarSerializer(cars, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, url_path="history", methods=["get"])
    def history(self, request, pk=None):
        history = ShopHistory.objects.filter(provider=pk)

        serializer = ShopHistorySerializer(history, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopSaleViewSet(viewsets.GenericViewSet):
    queryset = ShopSale.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopSaleSerializer

    def list(self, request):
        if request.user.user_type == 3:
            sales = self.get_queryset().filter(shop__user=request.user, is_active=True)
            serializer = self.get_serializer(sales, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "you don't have permission"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def retrieve(self, request, pk=None):
        if request.user.user_type == 3:
            sales = self.get_queryset().filter(
                shop__user=request.user, pk=pk, is_active=True
            )

            serializer = self.get_serializer(sales, many=True)

            if not serializer.data:
                return Response(
                    {"detail": "instance is inactive"},
                    status=status.HTTP_204_NO_CONTENT,
                )

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "you don't have permission"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        instance = self.get_object()

        instance.is_active = False
        instance.save()

        return Response(
            {"detail": "instance moved to inactive"},
            status=status.HTTP_205_RESET_CONTENT,
        )

    def update(self, request, pk=None):
        instance = self.get_object()
        if not instance.is_active:
            return Response(
                {"detail": "instance is inactive"}, status=status.HTTP_204_NO_CONTENT
            )

        if request.user.user_type in (3, 4) or request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            raise exceptions.PermissionDenied()

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
