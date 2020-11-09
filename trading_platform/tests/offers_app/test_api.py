from tests.fixtures import (
    client,
    get_urls,
    create_model_instance,
    get_root_page_data,
)

import pytest


@pytest.mark.django_db
def test_create_user_api(client, get_urls):
    # client creating
    url = get_urls['create-user']
    data = {'username': 'USER', 'password': 'PASSWORD', 'repeat_password': 'PASSWORD'}
    post_request = client.post(url, data=data, type='json')
    assert post_request.status_code == 201

    # client creating with wrong data
    url = get_urls['create-user']
    data = {'username': 'USER', 'password': 'PASSWORD', 'repeat_password': 'PASSWORD_'}
    post_request = client.post(url, data=data, type='json')
    assert post_request.status_code == 400


@pytest.mark.django_db
def test_currency_api(client, get_urls, create_model_instance):
    # records creating
    obj = create_model_instance(
        'Currency',
        {
            'code': 'CODE_1',
            'name': 'NAME_1'
        }
    )

    # non-authorized client
    # list
    data = [{'id': obj.pk,
             'code': obj.code,
             'name': obj.name}]
    url = get_urls['currencies']
    get_response = client.get(url)
    post_response = client.post(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert post_response.status_code == 401

    # detail
    data = {'id': obj.pk,
            'code': obj.code,
            'name': obj.name}
    url = get_urls['currencies'] + f'{obj.pk}/'
    get_response = client.get(url)
    post_response = client.post(url)
    delete_response = client.delete(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert post_response.status_code == 401
    assert delete_response.status_code == 401

    # authorized client
    user_data = {
        'username': 'USER',
        'password': 'PASSWORD'
    }
    user = create_model_instance('User', user_data)

    # login
    client.force_authenticate(user)

    # list
    data = [{'id': obj.pk,
             'code': obj.code,
             'name': obj.name}]
    url = get_urls['currencies']
    get_response = client.get(url)
    post_response = client.post(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert post_response.status_code == 403

    # detail
    data = {'id': obj.pk,
            'code': obj.code,
            'name': obj.name}
    url = get_urls['currencies'] + f'{obj.pk}/'
    get_response = client.get(url)
    put_response = client.put(url, data={'code': 'CODE_3', 'name': 'NAME_3'}, type='json')
    delete_response = client.delete(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert put_response.status_code == 403
    assert delete_response.status_code == 403

    # authorized client (superuser)
    user_data = {
        'username': 'SUPERUSER',
        'password': 'PASSWORD',
        'is_superuser': True,
    }
    superuser = create_model_instance('User', user_data)

    # login
    client.force_authenticate(superuser)

    # list
    data = [{'id': obj.pk,
             'code': obj.code,
             'name': obj.name}]
    input_data = {'code': 'CODE_2',
                  'name': 'NAME_2'}
    url = get_urls['currencies']
    get_response = client.get(url)
    post_response = client.post(url, data=input_data, type='json')
    assert get_response.status_code == 200
    assert get_response.data == data
    assert post_response.status_code == 201

    # detail
    data = {'id': obj.pk,
            'code': obj.code,
            'name': obj.name}
    url = get_urls['currencies'] + f'{obj.pk}/'
    get_response = client.get(url)
    put_response = client.put(url, data={'code': 'CODE_3', 'name': 'NAME_3'}, type='json')
    delete_response = client.delete(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert put_response.status_code == 200
    assert delete_response.status_code == 204


@pytest.mark.django_db
def test_item_api(client, get_urls, create_model_instance):
    # records creating
    currency = create_model_instance(
        'Currency',
        {
            'code': 'CODE_1',
            'name': 'NAME_1'
        }
    )
    item = create_model_instance(
        'Item',
        {
            'name': 'ITEM_1',
            'key': 'KEY_1',
            'currency': currency,
            'price': '100.00',
        }
    )

    # non-authorized client
    # list
    data = [{
        'id': item.pk,
        'name': 'ITEM_1',
        'key': 'KEY_1',
        'currency': currency.pk,
        'price': '100.00',
    }]
    url = get_urls['items']
    get_response = client.get(url)
    post_response = client.post(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert post_response.status_code == 401

    # detail
    data = {
        'id': item.pk,
        'name': 'ITEM_1',
        'key': 'KEY_1',
        'currency': currency.pk,
        'price': '100.00',
    }
    url = get_urls['items'] + f'{item.pk}/'
    get_response = client.get(url)
    post_response = client.post(url)
    delete_response = client.delete(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert post_response.status_code == 401
    assert delete_response.status_code == 401

    # authorized client
    user_data = {
        'username': 'USER',
        'password': 'PASSWORD'
    }
    user = create_model_instance('User', user_data)

    # login
    client.force_authenticate(user)

    # list
    data = [{
        'id': item.pk,
        'name': 'ITEM_1',
        'key': 'KEY_1',
        'currency': currency.pk,
        'price': '100.00',
    }]
    url = get_urls['items']
    get_response = client.get(url)
    post_response = client.post(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert post_response.status_code == 403

    # detail
    data = {
        'id': item.pk,
        'name': 'ITEM_1',
        'key': 'KEY_1',
        'currency': currency.pk,
        'price': '100.00',
    }
    url = get_urls['items'] + f'{item.pk}/'
    get_response = client.get(url)
    put_response = client.put(
        url,
        data={
            'name': 'ITEM_2',
            'key': 'KEY_2',
            'currency': currency.pk,
            'price': '200.00',
        },
        type='json'
    )
    delete_response = client.delete(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert put_response.status_code == 403
    assert delete_response.status_code == 403

    # authorized client (superuser)
    user_data = {
        'username': 'SUPERUSER',
        'password': 'PASSWORD',
        'is_superuser': True,
    }
    superuser = create_model_instance('User', user_data)

    # login
    client.force_authenticate(superuser)

    # list
    data = [{
        'id': item.pk,
        'name': 'ITEM_1',
        'key': 'KEY_1',
        'currency': currency.pk,
        'price': '100.00',
    }]
    input_data = {
        'name': 'ITEM_2',
        'key': 'KEY_2',
        'currency': currency.pk,
        'price': '200.00',
    }
    url = get_urls['items']
    get_response = client.get(url)
    post_response = client.post(url, data=input_data, type='json')
    assert get_response.status_code == 200
    assert get_response.data == data
    assert post_response.status_code == 201

    # detail
    data = {
        'id': item.pk,
        'name': 'ITEM_1',
        'key': 'KEY_1',
        'currency': currency.pk,
        'price': '100.00',
    }
    input_data = {
        'name': 'ITEM_3',
        'key': 'KEY_3',
        'currency': currency.pk,
        'price': '200.00',
    }
    url = get_urls['items'] + f'{item.pk}/'
    get_response = client.get(url)
    put_response = client.put(url, data=input_data, type='json')
    delete_response = client.delete(url)
    assert get_response.status_code == 200
    assert get_response.data == data
    assert put_response.status_code == 200
    assert delete_response.status_code == 204


@pytest.mark.django_db
def test_watch_lists_api_non_auth(client, get_urls, create_model_instance):
    # records creating
    owner = create_model_instance(
        'User',
        {
            'username': 'USER',
            'password': 'PASSWORD'
        }
    )
    currency = create_model_instance(
        'Currency',
        {
            'code': 'CODE_1',
            'name': 'NAME_1'
        }
    )
    item = create_model_instance(
        'Item',
        {
            'name': 'ITEM_1',
            'key': 'KEY_1',
            'currency': currency,
            'price': '100.00',
        }
    )
    watch_list = create_model_instance(
        'WatchList',
        {
            'owner': owner,
            'item': item,
        }
    )

    # list
    url = get_urls['watch-lists']
    get_response = client.get(url)
    post_response = client.post(url, data={'item': item.pk})
    assert get_response.status_code == 401
    assert post_response.status_code == 401

    # detail
    url = get_urls['watch-lists'] + f'{watch_list.pk}/'
    get_response = client.get(url)
    post_response = client.post(url)
    delete_response = client.delete(url)
    assert get_response.status_code == 401
    assert post_response.status_code == 401
    assert delete_response.status_code == 401


@pytest.mark.django_db
def test_watch_lists_api_auth(client, get_urls, create_model_instance):
    # records creating
    owner = create_model_instance(
        'User',
        {
            'username': 'USER',
            'password': 'PASSWORD'
        }
    )
    currency = create_model_instance(
        'Currency',
        {
            'code': 'CODE_1',
            'name': 'NAME_1'
        }
    )
    item = create_model_instance(
        'Item',
        {
            'name': 'ITEM_1',
            'key': 'KEY_1',
            'currency': currency,
            'price': '100.00',
        }
    )
    item_2 = create_model_instance(
        'Item',
        {
            'name': 'ITEM_2',
            'key': 'KEY_2',
            'currency': currency,
            'price': '100.00',
        }
    )
    watch_list = create_model_instance(
        'WatchList',
        {
            'owner': owner,
            'item': item,
        }
    )

    # login for owner
    client.force_authenticate(owner)

    # list
    url = get_urls['watch-lists']
    get_response = client.get(url)
    good_post_response = client.post(url, data={'item': item_2.pk}, type='json')
    bad_post_response = client.post(url, data={'item': item_2.pk}, type='json')
    assert get_response.status_code == 200
    assert get_response.data == [{'id': watch_list.pk, 'owner': owner.pk, 'item': item.pk}]
    assert good_post_response.status_code == 201
    assert bad_post_response.status_code == 400

    # detail
    url = get_urls['watch-lists'] + f'{watch_list.pk}/'
    get_response = client.get(url)
    good_put_response = client.put(url, data={'item': item.pk}, type='json')
    bad_put_response = client.put(url, data={'item': item_2.pk}, type='json')
    delete_response = client.delete(url)
    assert get_response.status_code == 200
    assert get_response.data == {'id': watch_list.pk, 'owner': owner.pk, 'item': item.pk}
    assert good_put_response.status_code == 200
    assert bad_put_response.status_code == 400
    assert delete_response.status_code == 204


@pytest.mark.django_db
def test_offer_api(client, get_urls, create_model_instance):
    # create offer record
    owner = create_model_instance(
        'User',
        {
            'username': 'USER',
            'password': 'PASSWORD'
        }
    )
    currency = create_model_instance(
        'Currency',
        {
            'code': 'CODE_1',
            'name': 'NAME_1'
        }
    )
    item = create_model_instance(
        'Item',
        {
            'name': 'ITEM_1',
            'key': 'KEY_1',
            'currency': currency,
            'price': '100.00',
        }
    )
    offer = create_model_instance(
        'Offer',
        {
            'owner': owner,
            'item': item,
            'number': 1000,
            'price': '10.00',
            'buy_or_sell': 'BUY',
            'is_active': True,
        }
    )

    # non-auth
    # list
    url = get_urls['offers']
    get_response = client.get(url)
    post_response = client.post(
        url,
        data=
        {
            'item': item.pk,
            'number': 900,
            'price': '10.00',
            'buy_or_sell': 'BUY',
            'is_active': True,
        }
        , type='json'
    )
    assert get_response.status_code == 200
    assert get_response.data == [{
        'id': offer.pk,
        'owner': owner.pk,
        'item': item.pk,
        'number': 1000,
        'price': '10.00',
        'buy_or_sell': 'BUY',
        'is_active': True,
    }]
    assert post_response.status_code == 401

    # detail
    url = get_urls['offers'] + f'{offer.pk}/'
    get_response = client.get(url)
    put_response = client.put(url)
    assert get_response.status_code == 200
    assert put_response.status_code == 401

    # auth
    # login
    client.force_authenticate(owner)

    # list
    url = get_urls['offers']
    get_response = client.get(url)
    post_response_1 = client.post(
        url,
        data=
        {
            'item': item.pk,
            'number': 900,
            'price': '10.00',
            'buy_or_sell': 'SELL',
            'is_active': True,
        }
        , type='json'
    )
    inventory = create_model_instance(
        'Inventory',
        {
            'owner': owner,
            'item': item,
            'number': 123,
        }
    )
    post_response_2 = client.post(
        url,
        data=
        {
            'item': item.pk,
            'number': 900,
            'price': '10.00',
            'buy_or_sell': 'SELL',
            'is_active': True,
        }
        , type='json'
    )
    post_response_3 = client.post(
        url,
        data=
        {
            'item': item.pk,
            'number': 100,
            'price': '10.00',
            'buy_or_sell': 'SELL',
            'is_active': True,
        }
        , type='json'
    )
    assert get_response.status_code == 200
    assert get_response.data == [{
        'id': offer.pk,
        'owner': owner.pk,
        'item': item.pk,
        'number': 1000,
        'price': '10.00',
        'buy_or_sell': 'BUY',
        'is_active': True,
    }]
    assert post_response_1.status_code == 400
    assert post_response_2.status_code == 400
    assert post_response_3.status_code == 201

    # detail
    url = get_urls['offers'] + f'{offer.pk}/'
    get_response = client.get(url)
    put_response = client.put(url,
                              data=
                              {
                                  'item': item.pk,
                                  'number': 800,
                                  'price': '10.00',
                                  'buy_or_sell': 'BUY',
                                  'is_active': True,
                              }
                              , type='json')
    assert get_response.status_code == 200
    assert put_response.status_code == 200


@pytest.mark.django_db
def test_trade_api(client, get_urls, create_model_instance):
    # create offer record
    customer = create_model_instance(
        'User',
        {
            'username': 'CUSTOMER',
            'password': 'PASSWORD'
        }
    )
    seller = create_model_instance(
        'User',
        {
            'username': 'SELLER',
            'password': 'PASSWORD'
        }
    )
    currency = create_model_instance(
        'Currency',
        {
            'code': 'CODE_1',
            'name': 'NAME_1'
        }
    )
    item = create_model_instance(
        'Item',
        {
            'name': 'ITEM_1',
            'key': 'KEY_1',
            'currency': currency,
            'price': '100.00',
        }
    )
    trade = create_model_instance(
        'Trade',
        {
            'customer': customer,
            'seller': seller,
            'item': item,
            'number': 100,
            'price': '120.00'
        }
    )

    # non-auth
    # list
    url = get_urls['trades']
    get_response = client.get(url)
    post_response = client.post(url)
    assert get_response.status_code == 200
    assert get_response.data == []
    assert post_response.status_code == 401

    # detail
    url = get_urls['trades'] + f'{trade.pk}/'
    get_response = client.get(url)
    put_response = client.get(url)
    assert get_response.status_code == 404
    assert put_response.status_code == 404

    # auth
    # login
    client.force_authenticate(customer)
    # list
    url = get_urls['trades']
    get_response = client.get(url)
    post_response = client.post(url)
    assert get_response.status_code == 200
    assert get_response.data == [{
        "id": trade.pk,
        "number": trade.number,
        "price": trade.price,
        "customer": trade.customer.pk,
        "seller": trade.seller.pk,
        "item": trade.item.pk,
    }]
    assert post_response.status_code == 403

    # detail
    url = get_urls['trades'] + f'{trade.pk}/'
    get_response = client.get(url)
    put_response = client.put(url)
    assert get_response.status_code == 200
    assert put_response.status_code == 403


@pytest.mark.django_db
def test_inventory_api(client, get_urls, create_model_instance):
    # records creating
    owner = create_model_instance(
        'User',
        {
            'username': 'USER',
            'password': 'PASSWORD'
        }
    )
    currency = create_model_instance(
        'Currency',
        {
            'code': 'CODE_1',
            'name': 'NAME_1'
        }
    )
    item = create_model_instance(
        'Item',
        {
            'name': 'ITEM_1',
            'key': 'KEY_1',
            'currency': currency,
            'price': '100.00',
        }
    )
    inventory = create_model_instance(
        'Inventory',
        {
            'owner': owner,
            'item': item,
            'number': 123,
        }
    )

    # non-auth
    # list
    url = get_urls['inventories']
    get_response = client.get(url)
    post_response = client.post(url)
    assert get_response.status_code == 200
    assert get_response.data == []
    assert post_response.status_code == 401

    # detail
    url = get_urls['inventories'] + f'{inventory.pk}/'
    get_response = client.get(url)
    put_response = client.get(url)
    assert get_response.status_code == 404
    assert put_response.status_code == 404

    # auth
    # login
    client.force_authenticate(owner)
    # list
    url = get_urls['inventories']
    get_response = client.get(url)
    post_response = client.post(url)
    assert get_response.status_code == 200
    assert get_response.data == [{
        "id": inventory.pk,
        'owner': owner.pk,
        'item': item.pk,
        'number': 123,
    }]
    assert post_response.status_code == 403

    # detail
    url = get_urls['inventories'] + f'{inventory.pk}/'
    get_response = client.get(url)
    put_response = client.put(url)
    assert get_response.status_code == 200
    assert put_response.status_code == 403


@pytest.mark.django_db
def test_user_api(client, get_urls, create_model_instance):
    user_1 = create_model_instance(
        'User',
        {
            'username': 'USER_1',
            'password': 'PASSWORD'
        }
    )
    user_2 = create_model_instance(
        'User',
        {
            'username': 'USER_2',
            'password': 'PASSWORD'
        }
    )

    # non-auth
    # list
    url = get_urls['users']
    get_response = client.get(url)
    post_response = client.post(url)
    assert get_response.status_code == 200
    assert get_response.data == [
        {
            'pk': user_1.pk,
            'username': user_1.username,
            'is_superuser': False,
        },
        {
            'pk': user_2.pk,
            'username': user_2.username,
            'is_superuser': False,
        }
    ]
    assert post_response.status_code == 401

    # detail
    url = get_urls['users'] + f'{user_1.pk}/'
    get_response = client.get(url)
    put_response = client.put(url)
    assert get_response.status_code == 200
    assert get_response.data == {
        'pk': user_1.pk,
        'username': user_1.username,
        'is_superuser': False,
    }
    assert put_response.status_code == 401

    # login
    client.force_authenticate(user_1)
    # list
    url = get_urls['users']
    get_response = client.get(url)
    post_response = client.post(url)
    assert get_response.status_code == 200
    assert get_response.data == [
        {
            'pk': user_1.pk,
            'username': user_1.username,
            'is_superuser': False,
        },
        {
            'pk': user_2.pk,
            'username': user_2.username,
            'is_superuser': False,
        }
    ]
    assert post_response.status_code == 403

    # detail
    url = get_urls['users'] + f'{user_1.pk}/'
    get_response = client.get(url)
    put_response = client.put(url)
    assert get_response.status_code == 200
    assert get_response.data == {
        'pk': user_1.pk,
        'username': user_1.username,
        'is_superuser': False,
    }
    assert put_response.status_code == 403


@pytest.mark.django_db
def test_root_api(client, get_urls, get_root_page_data):
    # non-authorized client
    url = get_urls['root']
    get_response = client.get(url)
    assert get_response.status_code == 200
    assert get_response.data == get_root_page_data

    # client creating
    url = get_urls['create-user']
    data = {'username': 'USER', 'password': 'PASSWORD', 'repeat_password': 'PASSWORD'}
    post_request = client.post(url, data=data, type='json')
    assert post_request.status_code == 201

    # login
    login_response = client.login(**data)
    assert login_response

    # authorized client
    url = get_urls['root']
    get_response = client.get(url)
    assert get_response.status_code == 200
    assert get_response.data == get_root_page_data
