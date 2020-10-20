from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from .serializers import *
from .permissions import IsOwnerOrReadOnlyUser
from django.contrib.auth.models import User


class CurrencyView(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ItemView(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class WatchListView(ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


class OfferView(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class TradeView(ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer


class InventoryView(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, IsOwnerOrReadOnlyUser)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return super().get_serializer_class()
