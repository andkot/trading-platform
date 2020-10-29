from django.contrib.auth.models import User

import pytest

from offers.models import (
    Currency,
    Item,
    WatchList,
    Offer,
    Trade,
    Inventory,
)


@pytest.fixture(autouse=True)
def set_up():
    # User
    User.objects.create(username='SUPERUSER', password='PASSWORD')
    User.objects.create(username='USER_1', password='PASSWORD')
    User.objects.create(username='USER_2', password='PASSWORD')

    # Currency
    Currency.objects.create(code='CODE_1', name='USD')
    Currency.objects.create(code='CODE_2', name='EUR')

    # Item
    Item.objects.create(name='ITEM_1',
                        key='KEY_1',
                        currency=Currency.objects.get(name='USD'),
                        price=12.50)
    Item.objects.create(name='ITEM_2',
                        key='KEY_2',
                        currency=Currency.objects.get(name='EUR'),
                        price=9.50)

    # WatchList
    WatchList.objects.create(owner=User.objects.get(username='USER_1'),
                             item=Item.objects.get(name='ITEM_1'))
    WatchList.objects.create(owner=User.objects.get(username='USER_1'),
                             item=Item.objects.get(name='ITEM_2'))
    WatchList.objects.create(owner=User.objects.get(username='USER_2'),
                             item=Item.objects.get(name='ITEM_1'))
    WatchList.objects.create(owner=User.objects.get(username='USER_2'),
                             item=Item.objects.get(name='ITEM_2'))

    # Offer
    Offer.objects.create(owner=User.objects.get(username='USER_1'),
                         item=Item.objects.get(name='ITEM_1'),
                         number=10,
                         price=9.65,
                         buy_or_sell='BUY',
                         is_active=True)
    Offer.objects.create(owner=User.objects.get(username='USER_1'),
                         item=Item.objects.get(name='ITEM_1'),
                         number=10,
                         price=10.65,
                         buy_or_sell='SELL',
                         is_active=True)
    Offer.objects.create(owner=User.objects.get(username='USER_2'),
                         item=Item.objects.get(name='ITEM_1'),
                         number=10,
                         price=9.65,
                         buy_or_sell='BUY',
                         is_active=True)
    Offer.objects.create(owner=User.objects.get(username='USER_1'),
                         item=Item.objects.get(name='ITEM_1'),
                         number=10,
                         price=12.65,
                         buy_or_sell='SELL',
                         is_active=True)

    # Trade
    Trade.objects.create(customer=User.objects.get(username='USER_1'),
                         seller=User.objects.get(username='USER_2'),
                         item=Item.objects.get(name='ITEM_1'),
                         number=43,
                         price=14.23)

    # Inventory
    Inventory.objects.create(owner=User.objects.get(username='USER_1'),
                             item=Item.objects.get(name='ITEM_1'),
                             number=12)
