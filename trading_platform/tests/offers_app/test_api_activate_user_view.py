from tests.fixtures import (
    client,
    get_urls,
    get_activate_url,
    get_django_mail,
    create_model_instance,
)

import pytest

from offers.api.tokens import make_token, decode_token


@pytest.mark.django_db
def test_activate_user_api(client, get_activate_url, get_django_mail, create_model_instance):
    user = create_model_instance(
        'User',
        {
            'username': 'USER_1',
            'email': 'test@foo.gmail',
            'password': 'PASSWORD'
        }
    )
    token = make_token(user)
    data = {'token': token}
    url = get_activate_url(token)['activate']
    get_request = client.get(url)
    assert get_request.status_code == 200
