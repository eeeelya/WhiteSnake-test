from rest_framework import permissions


class UpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "PUT" or request.method == "PATCH" and "balance" in request.data:
            if request.user.is_superuser or request.user.user_type == 4:
                return True
            return False
        return True


class IsProviderOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET" and request.user.user_type == 2:
            return True
        if request.method == "PUT" or "PATCH":
            if request.user.is_superuser or request.user.user_type == 2:
                return True
        return True
