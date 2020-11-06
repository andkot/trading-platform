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


class IsOwnerOrReadOnlyUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS) and (request.method not in 'POST'):
            return True
        return obj.pk == request.user.pk


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_superuser


class OnlySuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(pk=view.kwargs['pk'])
        return request.user == user

class IsOwnerOfTrade(permissions.BasePermission):
    def has_permission(self, request, view):
        v = view
        user = User.objects.get(pk=view.kwargs['pk'])
        return request.user == user
        # user = User.objects.filter() get(pk=view.kwargs['pk'])
        # return request.user == user
