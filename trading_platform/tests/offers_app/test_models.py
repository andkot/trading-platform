import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trading_platform.settings')
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import pytest

from offers.models import (
    Currency,
    Item,
    WatchList,
    Offer,
    Trade,
    Inventory,
)


class TestModels:
    @pytest.fixture()
    def set_up(self):
        Currency.objects.create(code='Code 1', name='USD')
        Currency.objects.create(code='Code 2', name='USD')

    @pytest.mark.django_db
    def currency_obj_creating(self):
        assert Currency.objects.count() == 2


# @pytest.mark.django_db
# def test_currency_model():
#     """Test Currency model"""
#
#     # Create Currency model instance
#     Currency.objects.create(code='Code 1', name='USD')
#     assert Currency.objects.count() == 1
