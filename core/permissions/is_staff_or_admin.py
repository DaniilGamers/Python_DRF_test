from rest_framework.permissions import BasePermission


class IsStaffOrAdmin(BasePermission):
    message = "Only staff or admin can block/unblock users."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))