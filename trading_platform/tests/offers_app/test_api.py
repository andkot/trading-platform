import pytest
from tests.fixtures import set_up
from rest_framework.test import APIClient

from offers.models import (
    Currency,
    Item,
    WatchList,
    Offer,
    Trade,
    Inventory,
)


@pytest.mark.django_db
def test_login(set_up):
    client = APIClient()

    # permissions
    # for SUPERUSER
    client.login(username='SUPERUSER', password='PASSWORD')
    # response = client.get('/myapi/api/')


@pytest.mark.django_db
def test_currency_view(set_up):
    client = APIClient()

    # get list
    response = client.get('/api/v1/currencies/')
    assert response.status_code == 200

    # get instance
    response = client.get('/api/v1/currencies/1/')
    assert response.status_code == 200
