from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission

from core.dataclasses.user_dataclass import User

UserModel: User = get_user_model()


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        user: User = request.user
        return user.is_seller


class IsSellerOrStaffOrAdmin(BasePermission):

    def has_permission(self, request, view):
        user: User = request.user
        return user.is_seller or user.is_staff or user.is_superuser


class IsAdminSuper(BasePermission):

    def has_permission(self, request, view):
        user: User = request.user
        return user.is_superuser
