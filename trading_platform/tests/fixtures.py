from rest_framework.test import APIClient
from rest_framework.reverse import reverse

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
from offers.enums import BuyOrSell

from offers.tasks import check_offers


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_model_instance():
    def _create_model_instance(model_name, data):
        models = {
            'User': User,
            'Currency': Currency,
            'Item': Item,
            'WatchList': WatchList,
            'Offer': Offer,
            'Trade': Trade,
            'Inventory': Inventory,
        }
        obj = models[model_name].objects.create(**data)
        return obj

    return _create_model_instance


@pytest.fixture
def get_urls():
    urls = {
        'root': reverse('offers:api-root'),
        'users': reverse('offers:users-list'),
        'create-user': reverse('offers:create-user-list'),
        'currencies': reverse('offers:currencies-list'),
        'items': reverse('offers:items-list'),
        'watch-lists': reverse('offers:watch-lists-list'),
        'offers': reverse('offers:offers-list'),
        'trades': reverse('offers:trades-list'),
        'inventories': reverse('offers:inventories-list'),
    }
    return urls


@pytest.fixture
def get_root_page_data(client, get_urls):
    server_name = client.request().wsgi_request.META['SERVER_NAME']
    data = {
        'currencies': f'http://{server_name}{get_urls["currencies"]}',
        'items': f'http://{server_name}{get_urls["items"]}',
        'watch-lists': f'http://{server_name}{get_urls["watch-lists"]}',
        'offers': f'http://{server_name}{get_urls["offers"]}',
        'trades': f'http://{server_name}{get_urls["trades"]}',
        'inventories': f'http://{server_name}{get_urls["inventories"]}',
        'users': f'http://{server_name}{get_urls["users"]}',
        'create-user': f'http://{server_name}{get_urls["create-user"]}'
    }
    return data


@pytest.fixture
def get_check_offers_task():
    return check_offers


@pytest.fixture
def get_inventory_instance():
    def _get_inventory_instance(pk):
        return Inventory.objects.get(id=pk)
    return _get_inventory_instance
