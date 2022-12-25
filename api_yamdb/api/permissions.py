from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission, AllowAny, IsAdminUser

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


class AdminPermissions(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_permission_object(self, request, view, obj):
        ...


class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_admin
