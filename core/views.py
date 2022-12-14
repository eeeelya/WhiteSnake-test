import requests
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.models import Car, User
from core.permissions import IsAdmin
from core.serializers import CarSerializer, UserSerializer


class UserInfoViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    def get_queryset(self):
        return User.objects.filter(is_active=True)

    def list(self, request):
        self.permission_classes = (IsAdmin,)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        instance = self.get_object()

        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAuthViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=["get"], url_path=r"activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)")
    def activate_account(self, request, uid, token):
        protocol = "https://" if request.is_secure() else "http://"
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/activation/"
        post_data = {"uid": uid, "token": token}
        headers = {"Authorization": f"Whitesnake {request.auth}"}
        response = requests.post(post_url, data=post_data, headers=headers)
        content = response.text

        if not content:
            content = "Account successfully verified"  # TODO change data message

        return Response(content, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path=r"password/reset/confirm/(?P<uid>[\w-]+)/(?P<token>[\w-]+)")
    def reset_password(self, request, uid, token):
        protocol = "https://" if request.is_secure() else "http://"
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/reset_password_confirm/"
        post_data = {"uid": uid, "token": token, "new_password": request.data["new_password"]}
        headers = {"Authorization": f"Whitesnake {request.auth}"}
        response = requests.post(post_url, data=post_data, headers=headers)
        content = response.text

        if not content:
            content = "Password changed successfully!"

        return Response(content, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path=r"username/reset/confirm/(?P<uid>[\w-]+)/(?P<token>[\w-]+)")
    def reset_password(self, request, uid, token):
        protocol = "https://" if request.is_secure() else "http://"
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/reset_username_confirm/"
        post_data = {"uid": uid, "token": token, "new_username": request.data["new_username"]}
        headers = {"Authorization": f"Whitesnake {request.auth}"}
        response = requests.post(post_url, data=post_data, headers=headers)
        content = response.text

        if not content:
            content = "Username changed successfully!"

        return Response(content, status=status.HTTP_200_OK)


class CarViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Car.objects.filter(is_active=True)

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
