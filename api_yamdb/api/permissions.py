from django.contrib.auth import get_user_model
from rest_framework.permissions import (SAFE_METHODS,
                                        BasePermission,)

User = get_user_model()


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in SAFE_METHODS
                )


class UserPermissions(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and request.user.is_user)


class ModeratorPermissions(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and request.user.is_moderator)


class AdminPermissions(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
        )


class ReviewPermission(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or (
                request.method == 'POST'
                and request.user.is_authenticated
            )
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAdminOrIsSelf(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_permission_object(self, request, view, obj):
        is_self = (request.user == obj)
        return request.method in SAFE_METHODS and (
            is_self or request.user.is_admin
        )


class AdminOrSuperUserPermissions(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )
