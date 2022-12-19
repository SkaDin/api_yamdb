from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in SAFE_METHODS)


class UserPermissions(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and request.user.is_user)

    def has_permission_object(self, request, view, obj):
        ...


class ModeratorPermissions(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and request.user.is_moderator)

    def has_permission_object(self, request, view, obj):
        ...


class AdminPermissions(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and request.user.is_admin)

    def has_permission_object(self, request, view, obj):
        ...