from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from django.urls import reverse as django_reverse

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

from offers.tasks import check_offers, send_mail


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User


@pytest.fixture
def jwt_urls():
    return {
        'obtain_jwt_token': django_reverse('offers:token-auth'),
        'refresh_jwt_token': django_reverse('offers:token-refresh'),
        'verify_jwt_token': django_reverse('offers:token-verify'),
    }


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
def get_activate_url():
    def _get_activate_url(data):
        urls = {
            'activate': reverse('offers:activate-activate', kwargs={'token': data}),
        }
        return urls

    return _get_activate_url


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


@pytest.fixture
def get_user_instance():
    def _get_user_instance(pk):
        return User.objects.get(id=pk)

    return _get_user_instance


@pytest.fixture
def email_backend_setup(settings):
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


@pytest.fixture
def get_django_mail():
    from django.core import mail
    return mail


@pytest.fixture
def get_send_email_task():
    return send_mail
