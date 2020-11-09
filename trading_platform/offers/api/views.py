from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from offers.api.permissions import (
    ReadOnly,
    IsOwnerOrReadOnly,
    IsSuperUserOrReadOnly,
    IsSuperUser,
)
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
from offers.api.filters import (
    IsOwnerFilter,
    IsBuyerOrSeller,
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
    permission_classes = (IsSuperUserOrReadOnly,)


class ItemView(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsSuperUserOrReadOnly,)


class WatchListView(ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (IsOwnerFilter,)


class OfferView(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def create(self, request, *args, **kwargs):
        target = request.data['buy_or_sell']
        if target == 'SELL':
            user_pk = request.user.pk
            item_pk = request.data['item']
            target_number = request.data['number']
            try:
                item = Inventory.objects.get(owner__id=user_pk, item_id=item_pk)
                number = item.number
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if number < int(target_number):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return super(OfferView, self).create(request, *args, **kwargs)

        return super(OfferView, self).create(request, *args, **kwargs)


class TradeView(ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = (ReadOnly,)
    filter_backends = (IsBuyerOrSeller,)


class InventoryView(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = (ReadOnly,)
    filter_backends = (IsOwnerFilter,)


class UsersListView(
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (ReadOnly,)


class CreateUserView(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_permissions(self):
        return (permissions.AllowAny(),)
