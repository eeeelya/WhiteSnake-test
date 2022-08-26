from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Car, User
from .serializers import CarSerializer, UserSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

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


class CarViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (AllowAny,)

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
