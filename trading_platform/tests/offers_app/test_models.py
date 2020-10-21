import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trading_platform.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import pytest

from offers.models import Currency


@pytest.mark.django_db
def test_currency_model():
    """Test Currency model"""

    # Create Currency model instance
    currency = Currency(code='Code 1', name='USD')
    currency1 = Currency(code='Code 1', name='USD')

    assert currency.code == 'Code 1'
    assert currency.code == currency1.code

    # assert (currency1 = Currency(code='Code 1', name='USD'))
