from tests.fixtures import (
    client,
    get_urls,
    get_django_mail,
)

import pytest


@pytest.mark.django_db
def test_create_user_api(client, get_urls, get_django_mail):
    # client creating
    url = get_urls['create-user']
    data = {
        'username': 'USER',
        'email': 'user@example.com',
        'password': 'PASSWORD',
        'repeat_password': 'PASSWORD'
    }
    post_request = client.post(url, data=data, type='json')
    assert post_request.status_code == 201
    assert len(get_django_mail.outbox) == 1

    # is not active by default
    from django.contrib.auth.models import User
    users = User.objects.all()
    assert not users.first().is_active

    # client creating with wrong data
    url = get_urls['create-user']
    data = {
        'username': 'USER',
        'email': 'user@example.com',
        'password': 'PASSWORD',
        'repeat_password': 'PASSWORD_'
    }
    post_request = client.post(url, data=data, type='json')
    assert post_request.status_code == 400
