from rest_framework import permissions


class IsOwnerOrReadOnlyUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS) and (request.method not in 'POST'):
            return True
        return obj.pk == request.user.pk


class IsNoSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in ('DELETE', 'POST', 'PUT', 'PATCH'):
            return True
        elif request.method in ('DELETE', 'POST', 'PUT', 'PATCH') and request.user.is_superuser:
            return True
        else:
            return False

    def has_permission(self, request, view):
        if view.action in ('create',) and request.user.is_superuser:
            return True
        return view.action not in ('create',)
