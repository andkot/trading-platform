from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, authentication
from rest_framework import status

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from offers.api.permissions import (
    ReadOnly,
    IsOwnerOrReadOnlyUser,
    IsSuperUserOrReadOnly,
    OnlySuperUser,
    IsOwner,
    IsOwnerOfTrade,
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
    permission_classes = (ReadOnly,)


class ItemView(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (ReadOnly,)


class WatchListView(ModelViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = (OnlySuperUser,)

    @action(detail=False, methods=['GET'], url_path='user-list/(?P<pk>[^/.]+)', )
    def user_list(self, request, pk):
        try:
            owner = self.queryset.filter(owner=User.objects.get(pk=pk))
            serializer = self.serializer_class(owner, many=True, context={'request': request})
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_permissions(self):
        if self.action == 'user_list':
            return (IsOwner(),)
        return (OnlySuperUser(),)


class OfferView(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyUser)


class TradeView(ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = (OnlySuperUser,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (IsOwnerOfTrade(),)
        return (OnlySuperUser(),)


class InventoryView(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class UsersListView(
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class DetailsUserView(
#
#     GenericViewSet,
# ):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class CreateUserView(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_permissions(self):
        return (permissions.AllowAny(),)
