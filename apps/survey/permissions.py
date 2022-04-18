from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
            
        if request.user.is_administrator or request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user in obj.users:
            return True
            
        if request.user.is_superuser or request.user.is_administrator:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False
