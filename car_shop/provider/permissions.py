from rest_framework import permissions


class IsAdminOrSuperUserForUpdate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "PUT":
            if request.user.is_superuser or request.user.user_type == 4:
                return True
            else:
                return False
        else:
            return True


class IsProviderOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            if request.user.user_type == 2:
                return True
            else:
                return False
        elif request.method in ("PUT", "PATCH"):
            if request.user.is_superuser or request.user.user_type == 2:
                return True
            else:
                return False
        else:
            return True
