from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from django.shortcuts import get_object_or_404
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


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def models_data():
    users_data = {
        'SUPERUSER': {'username': 'SUPERUSER', 'password': 'PASSWORD'},
        'USER_1': {'username': 'USER_1', 'password': 'PASSWORD'},
        'USER_2': {'username': 'USER_2', 'password': 'PASSWORD'},
        'USER_3': {'username': 'USER_3', 'password': 'PASSWORD'},
    }
    currencies_data = {
        'CURRENCY_1': {'code': 'CODE_1', 'name': 'NAME_1'},
        'CURRENCY_2': {'code': 'CODE_2', 'name': 'NAME_2'},
        'CURRENCY_3': {'code': 'CODE_3', 'name': 'NAME_3'},
    }
    items_data = {
        'ITEM_1': {'name': 'ITEM_1',
                   'key': 'KEY_1',
                   'currency': 'CURRENCY_1',
                   'price': '10.00'},
        'ITEM_2': {'name': 'ITEM_2',
                   'key': 'KEY_2',
                   'currency': 'CURRENCY_2',
                   'price': '20.00'},
        'ITEM_3': {'name': 'ITEM_3',
                   'key': 'KEY_3',
                   'currency': 'CURRENCY_3',
                   'price': '30.00'},
    }
    watch_lists_data = {
        'WATCH_LIST_1': {'owner': 'OWNER_1', 'item': 'ITEM_1'},
        'WATCH_LIST_2': {'owner': 'OWNER_2', 'item': 'ITEM_2'},
        'WATCH_LIST_3': {'owner': 'OWNER_3', 'item': 'ITEM_3'},
    }
    offers_data = {
        'OFFER_1': {'owner': 'USER_1',
                    'item': 'ITEM_1',
                    'number': 10,
                    'price': '9.00',
                    'buy_or_sell': BuyOrSell.BUY.value,
                    'is_active': True},
        'OFFER_2': {'owner': 'USER_1',
                    'item': 'ITEM_2',
                    'number': 10,
                    'price': '9.00',
                    'buy_or_sell': BuyOrSell.SELL.value,
                    'is_active': True},
        'OFFER_3': {'owner': 'USER_1',
                    'item': 'ITEM_1',
                    'number': 10,
                    'price': '8.00',
                    'buy_or_sell': BuyOrSell.BUY.value,
                    'is_active': True},
    }
    trades_data = {
        'TRADE_1':
            {'customer': 'USER_1',
             'seller': 'USER_2',
             'item': 'ITEM_1',
             'number': 43,
             'price': '14.23'},
    }
    return {
        'users_data': users_data,
        'currencies_data': currencies_data,
        'items_data': items_data,
        'watch_lists_data': watch_lists_data,
        'offers_data': offers_data,
        'trades_data': trades_data,
    }


@pytest.fixture
def get_model_instance():
    def _get_model_instance(model_name, is_superuser, data):
        models = {
            'User': User,
            'Currency': Currency,
            'Item': Item,
            'WatchList': WatchList,
            'Offer': Offer,
            'Trade': Trade,
            'Inventory': Inventory,
        }
        if is_superuser:
            obj = models[model_name].objects.create_superuser(**data)
            return obj
        obj = models[model_name].objects.create(**data)
        return obj

    return _get_model_instance


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
    }
    return urls


@pytest.fixture
def get_root_page_data(client):
    server_name = client.request().wsgi_request.META['SERVER_NAME']
    data = {
        'currencies': f'http://{server_name}/api/v1/currencies/',
        'items': f'http://{server_name}/api/v1/items/',
        'watch-lists': f'http://{server_name}/api/v1/watch-lists/',
        'offers': f'http://{server_name}/api/v1/offers/',
        'trades': f'http://{server_name}/api/v1/trades/',
        'inventories': f'http://{server_name}/api/v1/inventories/',
        'users': f'http://{server_name}/api/v1/users/',
        'create-user': f'http://{server_name}/api/v1/create-user/'
    }
    return data

# @pytest.fixture
# def user():
#     return User.objects.all()
#
#
# @pytest.fixture
# def set_pages_url():
#     def _set_pages_url(pk=None):
#         result = {
#             'url_currencies': reverse('offers:currencies-list'),
#             'url_user_creating': reverse('offers:user_creating-list'),
#             'url_main_page': reverse('offers:api-root')
#         }
#         if pk is not None:
#             result['url_user_details_by_pk'] = reverse('offers:users-detail', args=[pk, ]),
#             result['url_currency_details_by_pk'] = reverse('offers:currencies-detail', args=[pk, ]),
#
#         return result
#
#     return _set_pages_url


# @pytest.fixture
# def set_users_data():
#     user_data = {
#         'SUPERUSER': {'username': 'SUPERUSER', 'password': 'PASSWORD'},
#         'USER_1': {'username': 'USER_1', 'password': 'PASSWORD'},
#         'USER_2': {'username': 'USER_2', 'password': 'PASSWORD'},
#         'USER_3': {'username': 'USER_3', 'password': 'PASSWORD'},
#     }
#     return user_data
#
#
# @pytest.fixture
# def set_currencies_data():
#     currencies_data = {
#         'CURRENCY_1': {'code': 'CODE_1', 'name': 'NAME_1'},
#         'CURRENCY_2': {'code': 'CODE_2', 'name': 'NAME_2'},
#         'CURRENCY_3': {'code': 'CODE_3', 'name': 'NAME_3'},
#     }
#     return currencies_data
#
#
# @pytest.fixture
# def set_currencies(set_currencies_data):
#     currency_1_data = set_currencies_data['CURRENCY_1']
#     currency_1 = Currency.objects.create(code=currency_1_data['code'], name=currency_1_data['name'])
#
#     currency_2_data = set_currencies_data['CURRENCY_2']
#     currency_2 = Currency.objects.create(code=currency_2_data['code'], name=currency_2_data['name'])
#
#     currency_3_data = set_currencies_data['CURRENCY_3']
#     currency_3 = Currency.objects.create(code=currency_3_data['code'], name=currency_3_data['name'])
#
#     return {
#         'currency_1': currency_1,
#         'currency_2': currency_2,
#         'currency_3': currency_3,
#     }
#
#
# @pytest.fixture
# def set_superuser(client, set_users_data):
#     superuser_data = set_users_data['SUPERUSER']
#     superuser = User.objects.create_superuser(username=superuser_data['username'],
#                                               password=superuser_data['password'],
#                                               )
#     return superuser
#
#
# @pytest.fixture
# def superuser_client(client, set_users_data):
#     superuser_client = client
#     superuser_data = set_users_data['SUPERUSER']
#     superuser_data['repeat_password'] = superuser_data['password']
#     url_user_creating = reverse('offers:user_creating-list')
#     superuser_client.post(url_user_creating, data=superuser_data, format='json')
#     created_superuser = get_object_or_404(
#         User,
#         username=superuser_data['username'],
#     )
#     return superuser_client, created_superuser

# @pytest.fixture
# def set_up_user(set_users_data):
#     users_data = set_users_data
#     superuser = users_data['SUPERUSER']
#     user_1 = users_data['USER_1']
#     user_2 = users_data['USER_2']
#     user_3 = users_data['USER_3']
#     superuser = User.objects.create_superuser(username=superuser['username'], password=superuser['password'])
#     user_1 = User.objects.create(username=user_1['username'], password=user_1['password'])
#     user_2 = User.objects.create(username=user_2['username'], password=user_2['password'])
#     user_3 = User.objects.create(username=user_3['username'], password=user_3['password'])
#
#     return {'superuser': superuser,
#             'user_1': user_1,
#             'user_2': user_2,
#             'user_3': user_3,
#             }
#
#
# @pytest.fixture
# def set_up_currencies():
#     currency_1 = Currency.objects.create(code='CODE_1', name='USD')
#     currency_2 = Currency.objects.create(code='CODE_2', name='EUR')
#
#     return {'currency_1': currency_1, 'currency_2': currency_2}
#
#
# @pytest.fixture
# def set_up_items(set_up_currencies):
#     currency_1 = set_up_currencies['currency_1']
#     currency_2 = set_up_currencies['currency_2']
#
#     item_1 = Item.objects.create(
#         name='ITEM_1',
#         key='KEY_1',
#         currency=currency_1,
#         price=12.50
#     )
#     item_2 = Item.objects.create(
#         name='ITEM_2',
#         key='KEY_2',
#         currency=currency_2,
#         price=9.50
#     )
#
#     return {'item_1': item_1, 'item_2': item_2}
#
#
# @pytest.fixture
# def set_up_watch_list(set_up_items, set_up_user):
#     item_1 = set_up_items['item_1']
#     item_2 = set_up_items['item_2']
#
#     user_1 = set_up_user['user_1']
#     user_2 = set_up_user['user_2']
#
#     watch_list_1 = WatchList.objects.create(owner=user_1, item=item_1)
#     watch_list_2 = WatchList.objects.create(owner=user_1, item=item_2)
#     watch_list_3 = WatchList.objects.create(owner=user_2, item=item_1)
#     watch_list_4 = WatchList.objects.create(owner=user_2, item=item_2)
#
#     return {'watch_list_1': watch_list_1,
#             'watch_list_2': watch_list_2,
#             'watch_list_3': watch_list_3,
#             'watch_list_4': watch_list_4,
#             }
#
#
# @pytest.fixture
# def set_up_offers(set_up_user, set_up_items):
#     item_1 = set_up_items['item_1']
#     item_2 = set_up_items['item_2']
#
#     user_1 = set_up_user['user_1']
#     user_2 = set_up_user['user_2']
#
#     offer_1 = Offer.objects.create(owner=user_1,
#                                    item=item_1,
#                                    number=10,
#                                    price=9.65,
#                                    buy_or_sell=BuyOrSell.BUY.value,
#                                    is_active=True)
#     offer_2 = Offer.objects.create(owner=user_1,
#                                    item=item_1,
#                                    number=10,
#                                    price=10.65,
#                                    buy_or_sell=BuyOrSell.SELL.value,
#                                    is_active=True)
#     offer_3 = Offer.objects.create(owner=user_2,
#                                    item=item_1,
#                                    number=10,
#                                    price=9.65,
#                                    buy_or_sell=BuyOrSell.BUY.value,
#                                    is_active=True)
#     offer_4 = Offer.objects.create(owner=user_2,
#                                    item=item_2,
#                                    number=10,
#                                    price=12.65,
#                                    buy_or_sell=BuyOrSell.SELL.value,
#                                    is_active=True)
#
#     return {'offer_1': offer_1,
#             'offer_2': offer_2,
#             'offer_3': offer_3,
#             'offer_4': offer_4,
#             }
#
#
# @pytest.fixture
# def set_up_trades(set_up_user, set_up_items):
#     item_1 = set_up_items['item_1']
#
#     user_1 = set_up_user['user_1']
#     user_2 = set_up_user['user_2']
#
#     trade_1 = Trade.objects.create(customer=user_1,
#                                    seller=user_2,
#                                    item=item_1,
#                                    number=43,
#                                    price=14.23)
#
#     return {'trade_1': trade_1}
#
#
# @pytest.fixture
# def set_up_inventories(set_up_user, set_up_items):
#     item_1 = set_up_items['item_1']
#     user_1 = set_up_user['user_1']
#
#     inventory_1 = Inventory.objects.create(
#         owner=user_1,
#         item=item_1,
#         number=43,
#     )
#
#     return {'inventory_1': inventory_1}
#
#
# # Get URL
# @pytest.fixture
# def get_user_view_url(set_up_user):
#     users = set_up_user
#     user_1 = users['user_1']
#     return {
#         'list': reverse('offers:users-list'),
#         'detail': reverse('offers:user_details_or_create-detail', args=[user_1.pk]),
#     }
#
#
# @pytest.fixture
# def get_currency_view_url(set_up_currencies):
#     currencies = set_up_currencies
#     currency_1 = currencies['currency_1']
#     return {
#         'list': reverse('offers:currencies-list'),
#         'detail': reverse('offers:currencies-detail', args=[currency_1.pk]),
#     }
#
#
# @pytest.fixture
# def get_items_view_url(set_up_items):
#     return {
#         'list': reverse('offers:items-list'),
#         'detail': reverse('offers:items-detail', args=[set_up_items['item_1'].pk]),
#     }
#
#
# @pytest.fixture
# def get_watch_list_url(set_up_watch_list):
#     return {
#         'list': reverse('offers:watch_lists-list'),
#         'detail_1': reverse('offers:watch_lists-detail', args=[set_up_watch_list['watch_list_1'].pk]),
#         'detail_2': reverse('offers:watch_lists-detail', args=[set_up_watch_list['watch_list_2'].pk]),
#         'detail_3': reverse('offers:watch_lists-detail', args=[set_up_watch_list['watch_list_3'].pk]),
#         'detail_4': reverse('offers:watch_lists-detail', args=[set_up_watch_list['watch_list_4'].pk]),
#     }
#
#
# @pytest.fixture
# def get_offers_url(set_up_offers):
#     return {
#         'list': reverse('offers:offers-list'),
#         'detail_1': reverse('offers:offers-detail', args=[set_up_offers['offer_1'].pk]),
#         'detail_2': reverse('offers:offers-detail', args=[set_up_offers['offer_2'].pk]),
#         'detail_3': reverse('offers:offers-detail', args=[set_up_offers['offer_3'].pk]),
#         'detail_4': reverse('offers:offers-detail', args=[set_up_offers['offer_4'].pk]),
#     }
#
#
# @pytest.fixture
# def get_trades_url(set_up_trades):
#     return {
#         'list': reverse('offers:trades-list'),
#         'detail_1': reverse('offers:trades-detail', args=[set_up_trades['trade_1'].pk]),
#     }
#
#
# @pytest.fixture
# def get_inventories_url(set_up_inventories):
#     return {
#         'list': reverse('offers:inventories-list'),
#         'detail_1': reverse('offers:inventories-detail', args=[set_up_inventories['inventory_1'].pk]),
#     }
#
#
# # User and authentication
# @pytest.fixture
# def superuser_client(client, set_up_user, ):
#     superuser = set_up_user['superuser']
#     user_pk = set_up_user['superuser'].pk
#     url = reverse('offers:token_auth')
#     drf_url = reverse('rest_framework:login')
#     user_url = reverse('offers:user_details_or_create-detail',
#                        args=[set_up_user['superuser'].pk])
#     data = {'username': 'SUPERUSER', 'password': 'PASSWORD'}
#     response = client.post(user_url, data=data, format='json')
#     # active_token = response.data['token']
#     # client.credentials(HTTP_AUTHORIZATION=f'Bearer {active_token}')
#
#     # pk = User.objects.get(username='SUPERUSER').pk
#     # response = client.post(reverse('/api/v1/auth/login/'), data={'username': 'SUPERUSER', 'password': 'PASSWORD'})
#     # response = client.get('/api/v1/users/pk')
#
#     # assert response.status_code == 302
#     return {
#         'client': client,
#         'superuser': superuser,
#         'user_url': user_url,
#         'drf_url': drf_url,
#         'data': data
#     }
