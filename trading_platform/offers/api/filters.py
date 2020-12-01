from rest_framework.filters import BaseFilterBackend

from django.db.models import Q


class IsOwnerFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner__id=request.user.id)


class IsBuyerOrSeller(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(customer__id=request.user.id) | Q(seller__id=request.user.id))
