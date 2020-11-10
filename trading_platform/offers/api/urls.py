from offers.api.views import (
    CurrencyView,
    ItemView,
    WatchListView,
    OfferView,
    TradeView,
    InventoryView,
    UsersListView,
    CreateUserView,
)

from rest_framework import routers

from django.urls import path, include

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.conf.urls import url

app_name = 'offers'

router = routers.DefaultRouter()

router.register(r'currencies', CurrencyView, basename='currencies')
router.register(r'items', ItemView, basename='items')
router.register(r'watch-lists', WatchListView, basename='watch-lists')
router.register(r'offers', OfferView, basename='offers')
router.register(r'trades', TradeView, basename='trades')
router.register(r'inventories', InventoryView, basename='inventories')
router.register(r'users', UsersListView, basename='users')
router.register(r'create-user', CreateUserView, basename='create-user')

urlpatterns = router.urls

urlpatterns += url(r'^api-token-auth/', obtain_jwt_token, name='token_auth'),
urlpatterns += url(r'^api-token-refresh/', refresh_jwt_token, name='token_refresh'),
