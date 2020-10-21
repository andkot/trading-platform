from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from offers.api.permissions import IsOwnerOrReadOnlyUser
from offers.api.serializers import (
    CurrencySerializer,
    ItemSerializer,
    WatchListSerializer,
    OfferSerializer,
    TradeSerializer,
    InventorySerializer,
    CreateUserSerializer,
    UserSerializer,
)
from offers.models import (
    Currency,
    Item,
    WatchList,
    Offer,
    Trade,
    Inventory,
)

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

    @action(detail=False, methods=['GET'], url_path='user_list/(?P<pk>[^/.]+)')
    def user_list(self, request, pk):
        try:
            owner = self.queryset.filter(owner=User.objects.get(pk=pk))
            serializer = self.serializer_class(owner, many=True, context={'request': request})
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class OfferView(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


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

# from ..asynchrony.test_task import hello_world
#
#
# class AsyncView(ModelViewSet):
#     queryset = Currency.objects.all()
#     serializer_class = CurrencySerializer
#
#     @action(detail=False, methods=['GET'])
#     def test(self, request):
#         return Response({'test': hello_world()})
