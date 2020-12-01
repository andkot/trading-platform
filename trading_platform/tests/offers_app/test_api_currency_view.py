from tests.fixtures import (
    client,
    get_urls,
    create_model_instance,
    get_root_page_data,
)

import pytest


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
    data = [
        {
            'id': obj.pk,
            'code': obj.code,
            'name': obj.name
        }
    ]
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
