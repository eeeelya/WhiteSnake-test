from rest_framework import permissions


class UpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "PUT" or request.method == "PATCH" and "balance" in request.data:
            if request.user.is_superuser or request.user.user_type == 4:
                return True
            return False
        else:
            return True