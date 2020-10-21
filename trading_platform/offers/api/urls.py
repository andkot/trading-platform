from .views import (
    CurrencyView,
    ItemView,
    WatchListView,
    OfferView,
    TradeView,
    InventoryView,
    UserView,
)

from rest_framework import routers

from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'currencies', CurrencyView)
router.register(r'items', ItemView)
router.register(r'watch_lists', WatchListView)
router.register(r'offers', OfferView)
router.register(r'trades', TradeView)
router.register(r'inventories', InventoryView)
router.register(r'users', UserView)

urlpatterns = router.urls
urlpatterns.append(path('auth/', include('rest_framework.urls', namespace='rest_framework')))
