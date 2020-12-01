from offers.api.views import (
    CurrencyView,
    ItemView,
    WatchListView,
    OfferView,
    TradeView,
    InventoryView,
    UsersListView,
    CreateUserView,
    ActivateUserView,
    UpdateUserView,
)

from rest_framework import routers

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
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
router.register(r'activate', ActivateUserView, basename='activate')
router.register(r'update', UpdateUserView, basename='update')

urlpatterns = router.urls

# urlpatterns += url(r'^api-token-auth/', obtain_jwt_token, name='token-auth'),
# urlpatterns += url(r'^api-token-refresh/', refresh_jwt_token, name='token-refresh'),
# urlpatterns += url(r'^api-token-verify/', verify_jwt_token, name='token-verify'),
