from rest_framework import exceptions, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Client, ClientCar
from .serializers import ClientCarSerializer, ClientSerializer


class ClientViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(
                {"detail": "0 active instances"}, status=status.HTTP_204_NO_CONTENT
            )

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        if instance.is_active:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(
                {"detail": "instance is inactive"}, status=status.HTTP_204_NO_CONTENT
            )

    def destroy(self, request, pk=None):
        instance = self.get_object()

        if not instance.is_active:
            return Response(
                {"detail": "instance is inactive"},
                status=status.HTTP_205_RESET_CONTENT,
            )

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
        cars = ClientCar.objects.filter(provider=pk)

        serializer = ClientCarSerializer(cars, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "client doesn't have cars"}, status=status.HTTP_200_OK
            )

    @action(detail=True, url_path="history", methods=["get"])
    def history(self, requested):
        pass
