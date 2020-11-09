from django.contrib.auth.models import User

from rest_framework import permissions
from rest_framework.reverse import reverse


class IsAuthenticatedOrAPIRoot(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        api_root_view = (request.method == 'GET') and (request.META['PATH_INFO'] == reverse('offers:api-root'))
        return api_root_view


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or (request.method == 'GET')

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS) and (request.method not in 'POST'):
            return True
        return obj.owner.pk == request.user.pk


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_superuser


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner.pk == request.user.pk


class IsOwnerToCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ('create', 'list'):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.owner.pk == request.user.pk


class IsOwnerOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(pk=view.kwargs['pk'])
        except:
            return request.user.is_superuser
        return (request.user == user) or request.user.is_superuser
