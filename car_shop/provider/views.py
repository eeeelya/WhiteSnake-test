from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Provider, ProviderCar, ProviderHistory, ProviderSale
from .serializers import ProviderCarSerializer, ProviderHistorySerializer, ProviderSaleSerializer, ProviderSerializer


class ProviderViewSet(viewsets.GenericViewSet):
    queryset = Provider.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProviderSerializer

    def list(self, request):
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

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
        cars = ProviderCar.objects.filter(provider=pk)

        serializer = ProviderCarSerializer(cars, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, url_path="history", methods=["get"])
    def history(self, request, pk=None):
        history = ProviderHistory.objects.filter(provider=pk)

        serializer = ProviderHistorySerializer(history, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProviderSaleViewSet(viewsets.GenericViewSet):
    queryset = ProviderSale.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProviderSaleSerializer

    def list(self, request):
        if request.user.user_type == 2:
            sales = self.get_queryset().filter(
                provider__user=request.user, is_active=True
            )
            serializer = self.get_serializer(sales, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "you don't have permission"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def retrieve(self, request, pk=None):
        if request.user.user_type == 2:
            sales = self.get_queryset().filter(
                provider__user=request.user, pk=pk, is_active=True
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

        if request.user.user_type in (2, 4) or request.user.is_superuser:
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
