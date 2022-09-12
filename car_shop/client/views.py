from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from client.filters import ClientFilter
from client.models import Client
from client.permissions import IsAdminOrSuperUserForUpdate
from client.serializers import ClientSerializer
from django_filters.rest_framework import DjangoFilterBackend
from shop.models import ShopHistory
from shop.serializers import ShopHistorySerializer


class ClientViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated, IsAdminOrSuperUserForUpdate)
    filter_backends = (DjangoFilterBackend,)
    filter_class = ClientFilter

    def get_queryset(self):
        return Client.objects.filter(is_active=True)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "no active instances"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
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
    def history(self, request, pk=None):
        cars = ShopHistory.objects.filter(client__user=request.user)

        serializer = ShopHistorySerializer(cars, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "client doesn't have history"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        pass
