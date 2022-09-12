from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Car, User
from core.serializers import CarSerializer, UserSerializer


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return User.objects.filter(is_active=True)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No active instances"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        instance = self.get_object()

        instance.is_active = False
        instance.save()

        return Response({"detail": "instance moved to inactive"}, status=status.HTTP_200_OK)


class CarViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Car.objects.filter(is_active=True)

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

    def delete(self, request, pk=None):
        instance = self.get_object()

        if not instance.is_active:
            return Response({"detail": "instance is inactive"}, status=status.HTTP_400_BAD_REQUEST)

        instance.is_active = False
        instance.save()

        return Response({"detail": "instance moved to inactive"}, status=status.HTTP_200_OK)
