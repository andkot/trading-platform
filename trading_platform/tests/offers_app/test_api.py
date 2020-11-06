from tests.fixtures import (
    client,
    models_data,
    get_model_instance,
    get_urls,
    get_root_page_data,
)

import pytest


@pytest.mark.django_db
def test_non_auth_client(client, models_data, get_model_instance, get_urls, get_root_page_data):
    currencies_data = models_data['currencies_data']
    currency_data = currencies_data['CURRENCY_1']

    # root url
    url = get_urls['root']
    response = client.get(url)
    root_page_data = get_root_page_data
    assert response.status_code == 200
    assert response.data == root_page_data

    # currencies list view
    url = get_urls['currencies']
    get_response = client.get(url)
    post_response = client.post(url, data=currency_data, type='json')
    assert get_response.status_code == 200
    assert post_response.status_code == 401

    # test currency details view
    currency = get_model_instance('Currency', False, currency_data)
    url = get_urls['currencies'] + f'{currency.pk}/'
    data = currency_data
    data['id'] = currency.pk
    get_response = client.get(url)
    del_response = client.delete(url)
    put_response = client.put(url)
    post_response = client.post(url)
    patch_response = client.patch(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert del_response.status_code == 401
    assert put_response.status_code == 401
    assert post_response.status_code == 401
    assert patch_response.status_code == 401

    # test creating user
    users_data = models_data['users_data']
    user_data = users_data['USER_1']
    user_data['repeat_password'] = 'INCORRECT_PASSWORD'
    url = get_urls['create-user']
    get_response = client.get(url)
    bad_post_request = client.post(url, data=user_data, type='json')
    user_data['repeat_password'] = user_data['password']
    good_post_request = client.post(url, data=user_data, type='json')
    assert get_response.status_code == 405
    assert bad_post_request.status_code == 400
    assert good_post_request.status_code == 201

    # test items list view
    url = get_urls['items']
    items_data = models_data['items_data']
    item_data = items_data['ITEM_1']
    get_response = client.get(url)
    post_response = client.post(url, data=item_data, type='json')
    assert get_response.status_code == 200
    assert post_response.status_code == 401

    # test item details view
    item_data['currency'] = currency
    item = get_model_instance('Item', False, item_data)
    url = get_urls['items'] + f'{item.pk}/'
    data = item_data
    data['id'] = item.pk
    data['currency'] = currency.pk
    get_response = client.get(url)
    del_response = client.delete(url)
    put_response = client.put(url)
    post_response = client.post(url)
    patch_response = client.patch(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert del_response.status_code == 401
    assert put_response.status_code == 401
    assert post_response.status_code == 401
    assert patch_response.status_code == 401

    # test watch_lists list view
    url = get_urls['watch-lists']
    watch_lists_data = models_data['watch_lists_data']
    watch_list_data = watch_lists_data['WATCH_LIST_1']
    get_response = client.get(url)
    post_response = client.post(url, data=watch_list_data, type='json')
    assert get_response.status_code == 401
    assert post_response.status_code == 401

    # test watch_list details view
    user_data = users_data['USER_2']
    watch_list_data['item'] = item
    user = get_model_instance('User', False, user_data)
    watch_list_data['owner'] = user
    watch_list = get_model_instance('WatchList', False, watch_list_data)
    url = get_urls['watch-lists'] + f'{watch_list.pk}/'
    # data = watch_list_data
    # data['item'] = item.pk
    # data['owner'] = user.pk
    get_response = client.get(url)
    del_response = client.delete(url)
    put_response = client.put(url)
    post_response = client.post(url)
    patch_response = client.patch(url)
    assert get_response.status_code == 401
    # assert get_response.data == data
    assert del_response.status_code == 401
    assert put_response.status_code == 401
    assert post_response.status_code == 401
    assert patch_response.status_code == 401

    # test offers list view
    url = get_urls['offers']
    offers_data = models_data['offers_data']
    offer_data = offers_data['OFFER_1']
    get_response = client.get(url)
    post_response = client.post(url, data=offer_data, type='json')
    assert get_response.status_code == 200
    assert post_response.status_code == 401

    # test offer details view
    watch_list_data['item'] = item
    offer_data['owner'] = user
    offer_data['item'] = item
    offer = get_model_instance('Offer', False, offer_data)
    url = get_urls['offers'] + f'{offer.pk}/'
    data = offer_data
    data['owner'] = user.pk
    data['item'] = item.pk
    data['id'] = offer.pk
    get_response = client.get(url)
    del_response = client.delete(url)
    put_response = client.put(url)
    post_response = client.post(url)
    patch_response = client.patch(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert del_response.status_code == 401
    assert put_response.status_code == 401
    assert post_response.status_code == 401
    assert patch_response.status_code == 401

    # test trades list view
    url = get_urls['trades']
    trades_data = models_data['trades_data']
    trade_data = trades_data['OFFER_1']
    get_response = client.get(url)
    post_response = client.post(url, data=trade_data, type='json')
    assert get_response.status_code == 200
    assert post_response.status_code == 401

    # test trade details view
    watch_list_data['item'] = item
    offer_data['owner'] = user
    offer_data['item'] = item
    offer = get_model_instance('Offer', False, offer_data)
    url = get_urls['offers'] + f'{offer.pk}/'
    data = offer_data
    data['owner'] = user.pk
    data['item'] = item.pk
    data['id'] = offer.pk
    get_response = client.get(url)
    del_response = client.delete(url)
    put_response = client.put(url)
    post_response = client.post(url)
    patch_response = client.patch(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert del_response.status_code == 401
    assert put_response.status_code == 401
    assert post_response.status_code == 401
    assert patch_response.status_code == 401


@pytest.mark.django_db
def test_auth_client(client, models_data, get_model_instance, get_urls):
    users_data = models_data['users_data']
    user_data = users_data['USER_1']

    # user creating
    url = get_urls['create-user']
    user_data['repeat_password'] = user_data['password']
    post_request = client.post(url, data=user_data, type='json')
    del user_data['repeat_password']
    assert post_request.status_code == 201

    # test login
    login_response = client.login(**user_data)
    assert login_response

    # currencies list view
    currencies_data = models_data['currencies_data']
    currency_data = currencies_data['CURRENCY_1']
    url = get_urls['currencies']
    get_response = client.get(url)
    post_response = client.post(url, data=currency_data, type='json')
    assert get_response.status_code == 200
    assert post_response.status_code == 403

    # currency details view
    currency = get_model_instance('Currency', False, currency_data)
    url = get_urls['currencies'] + f'{currency.pk}/'
    data = currency_data
    data['id'] = currency.pk
    get_response = client.get(url)
    del_response = client.delete(url)
    put_response = client.put(url)
    post_response = client.post(url)
    patch_response = client.patch(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert del_response.status_code == 403
    assert put_response.status_code == 403
    assert post_response.status_code == 403
    assert patch_response.status_code == 403

# @pytest.mark.django_db
# def test_user(client, set_pages_url, set_users_data, user):
#     user_client = client
#     user_data = set_users_data['USER_1']
#
#     # repeat_password is correct
#     user_data['repeat_password'] = user_data['password']
#     url_user_creating = set_pages_url()['url_user_creating']
#     good_response = user_client.post(url_user_creating, data=user_data, format='json')
#
#     # repeat_password isn't correct
#     user_data['repeat_password'] = 'INCORRECT'
#     bad_response = user_client.post(url_user_creating, data=user_data, format='json')
#
#     assert good_response.status_code == 201
#     assert bad_response.status_code == 400
#
#     # test login
#     login_response = user_client.login(username=user_data['username'],
#                                        password=user_data['password'])
#     assert login_response == True
#
#     # test getting details
#     user_pk = user.get(username=user_data['username']).pk
#     data = {'username': user_data['username'], 'is_superuser': False, 'pk': user_pk}
#     url = set_pages_url(user_pk)['url_user_details_by_pk']
#     details_response = user_client.get(url)
#     assert details_response.status_code == 200
#     assert details_response.data == data
#
#
# @pytest.mark.django_db
# def test_superuser(client, set_pages_url, set_users_data, set_superuser):
#     superuser_client = client
#     superuser_data = set_users_data['SUPERUSER']
#     superuser = set_superuser
#
#     # test login
#     login_response = superuser_client.login(username=superuser_data['username'],
#                                             password=superuser_data['password'])
#     assert login_response == True
#
#     # test getting details
#     data = {'username': superuser.username, 'is_superuser': superuser.is_superuser, 'pk': superuser.pk}
#     url = set_pages_url(superuser.pk)['url_user_details_by_pk']
#     details_response = superuser_client.get(url)
#     assert details_response.status_code == 200
#     assert details_response.data == data
#
#     # test getting main page
#     server_name = superuser_client.request().wsgi_request.META['SERVER_NAME']
#     data = {
#         'currencies': f'http://{server_name}/api/v1/currencies/',
#         'items': f'http://{server_name}/api/v1/items/',
#         'watch_lists': f'http://{server_name}/api/v1/watch_lists/',
#         'offers': f'http://{server_name}/api/v1/offers/',
#         'trades': f'http://{server_name}/api/v1/trades/',
#         'inventories': f'http://{server_name}/api/v1/inventories/',
#         'users': f'http://{server_name}/api/v1/users/',
#         'users-create': f'http://{server_name}/api/v1/users-create/'
#     }
#     url = set_pages_url()['url_main_page']
#     main_page_response = superuser_client.get(url)
#     assert main_page_response.status_code == 200
#     assert main_page_response.data == data

# urls = get_user_view_url
# list_url, detail_url = urls['list'], urls['detail']

# response = client.get(list_url)
# assert response.status_code == 200

# response = client.get(detail_url)
# assert response.status_code == 200

# @pytest.mark.django_db
# def test_currency_view(set_up_currencies, client, get_currency_view_url):
#     urls = get_currency_view_url
#     list_url, detail_url = urls['list'], urls['detail']
#
#     response = client.get(list_url)
#     assert response.status_code == 200
#
#     response = client.get(detail_url)
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_item_view(set_up_items, client, get_items_view_url):
#     urls = get_items_view_url
#     list_url, detail_url = urls['list'], urls['detail']
#
#     response = client.get(list_url)
#     assert response.status_code == 200
#
#     response = client.get(detail_url)
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_watch_list_view(
#         set_up_user,
#         set_up_watch_list,
#         get_watch_list_url,
#         superuser_client):
#     urls = get_watch_list_url
#     list_url = urls['list']
#     detail_url_1 = urls['detail_1']
#
#     # superuser = set_up_user['superuser']
#
#     # force_authenticate(client.get(list_url), user=superuser)
#     response = superuser_client['client'].login(
#         username='SUPERUSER',
#         password='PASSWORD'
#     )
#     response = superuser_client['client'].get(list_url)
#     assert response.status_code == 200
#
#     response = client.get(detail_url_1)
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_offers_view(set_up_user, set_up_items, client, get_offers_url):
#     urls = get_offers_url
#     list_url = urls['list']
#     detail_url_1 = urls['detail_1']
#
#     response = client.get(list_url)
#     assert response.status_code == 200
#
#     response = client.get(detail_url_1)
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_trades_view(set_up_user, set_up_items, set_up_trades, client, get_trades_url):
#     urls = get_trades_url
#     list_url = urls['list']
#     detail_url_1 = urls['detail_1']
#
#     response = client.get(list_url)
#     assert response.status_code == 200
#
#     response = client.get(detail_url_1)
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_inventories_view(set_up_user, set_up_items, set_up_inventories, client, get_inventories_url):
#     urls = get_inventories_url
#     list_url = urls['list']
#     detail_url_1 = urls['detail_1']
#
#     response = client.get(list_url)
#     assert response.status_code == 200
#
#     response = client.get(detail_url_1)
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_superuser_login(set_up_user, superuser_client, client):
#     superuser = superuser_client
#     res = superuser_client
#     client.login(username='SUPERUSER', password='PASSWORD')
#     response = client.get('/api/v1/users/pk')
#     # assert response.status_code == 200
