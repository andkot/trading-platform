from tests.fixtures import (
    client,
    get_urls,
    create_model_instance,
    get_root_page_data,
    get_user_instance,
    user,
jwt_urls,
)

import pytest


@pytest.mark.django_db
def test_user_api(client, get_urls, user, jwt_urls):
    user_1 = user.objects.create_user(username='user', email='user@foo.com', password='pass')
    user_1.is_active = False
    user_1.save()

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

    # auth
    url = jwt_urls['obtain_jwt_token']
    resp = client.post(url, data={
        'username': 'user',
        'password': 'pass'
    }, format='json')
    assert resp.status_code == 400

    user_1.is_active = True
    user_1.save()
    resp = client.post(url, data={
        'username': 'user',
        'password': 'pass'
    }, format='json')
    assert resp.status_code == 200

    token = resp.data['token']
    verification_url = jwt_urls['verify_jwt_token']
    resp = client.post(verification_url, {'token': token}, format='json')
    assert resp.status_code == 200

    verification_url = jwt_urls['verify_jwt_token']
    resp = client.post(verification_url, {'token': 'abs'}, format='json')
    assert resp.status_code == 400

    url = get_urls['users'] + f'{user_1.pk}/'
    resp = client.post(url, data={'username': 'user', 'password': 'pass_'}, format='json')
    assert resp.status_code == 401

    # add credentials
    verification_url = jwt_urls['verify_jwt_token']
    resp = client.post(verification_url, {'token': token}, format='json')
    assert resp.status_code == 200

    client.credentials(HTTP_AUTHORIZATION=f'JWT abs')
    url = get_urls['users'] + f'{user_1.pk}/'
    resp = client.put(url, data={'username': 'user_', 'password': 'pass'}, format='json')
    assert resp.status_code == 401

    client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
    url = get_urls['users'] + f'{user_1.pk}/'
    resp = client.put(url, data={'username': 'user_', 'password': 'pass'}, format='json')
    assert resp.status_code == 200

    user_2 = user.objects.create_user(username='user_2', email='user@foo.com', password='pass')
    user_2.is_active = True
    user_2.save()
    url = get_urls['users'] + f'{user_2.pk}/'
    resp = client.post(url, data={'format': 'json'})
    assert resp.status_code == 401
    # self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # # list
    # url = get_urls['users']
    # get_response = client.get(url)
    # post_response = client.post(url)
    # assert get_response.status_code == 200
    # assert get_response.data == [
    #     {
    #         'pk': user_1.pk,
    #         'username': user_1.username,
    #         'is_superuser': False,
    #     },
    #     {
    #         'pk': user_2.pk,
    #         'username': user_2.username,
    #         'is_superuser': False,
    #     }
    # ]
    # assert post_response.status_code == 403
    #
    # # detail
    # url = get_urls['users'] + f'{user_1.pk}/'
    # get_response = client.get(url)
    # put_response = client.put(url)
    # assert get_response.status_code == 200
    # assert get_response.data == {
    #     'pk': user_1.pk,
    #     'username': user_1.username,
    #     'is_superuser': False,
    # }
    # assert put_response.status_code == 403
