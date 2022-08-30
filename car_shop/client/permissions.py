from rest_framework import permissions


class IsAdminOrSuperUserForUpdate(permissions.BasePermission):
    edit_method = "PUT"

    def has_permission(self, request, view):
        if request.method == self.edit_method:
            if request.user.is_superuser or request.user.user_type == 4:
                return True
            else:
                return False
        else:
            return True
