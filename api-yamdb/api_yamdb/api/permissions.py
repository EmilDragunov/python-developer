from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка прав администратора."""

    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_admin or request.user.is_superuser
        )


class IsOwnerOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
            or obj.author == request.user
        )
