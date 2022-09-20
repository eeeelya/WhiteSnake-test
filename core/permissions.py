from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if view.action == "list":
            return request.user.is_superuser or request.user.user_type == 4
        return True
