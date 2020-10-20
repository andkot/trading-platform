from .views import *
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'currency', CurrencyView)
router.register(r'item', ItemView)
router.register(r'watch_list', WatchListView)
router.register(r'offer', OfferView)
router.register(r'trade', TradeView)
router.register(r'inventory', InventoryView)
router.register(r'user', UserView)

urlpatterns = router.urls
urlpatterns.append(path('auth/', include('rest_framework.urls', namespace='rest_framework')))
