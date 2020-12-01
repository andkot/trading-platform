from tests.fixtures import (
    create_model_instance,
    get_check_offers_task,
    get_inventory_instance,
    get_send_email_task,
    get_django_mail,
)

import pytest


@pytest.mark.django_db
def test_offers(
        create_model_instance,
        get_check_offers_task,
        get_inventory_instance
):
    # data
    buyer = create_model_instance(
        'User',
        {
            'username': 'BUYER',
            'password': 'PASSWORD',
        },
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
            'name': 'NAME_1',
        },
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
    inventory_sell = create_model_instance(
        'Inventory',
        {
            'owner': seller,
            'item': item,
            'number': 2000,
        }
    )
    offer_sell = create_model_instance(
        'Offer',
        {
            'owner': seller,
            'item': item,
            'number': 1100,
            'price': '10.00',
            'buy_or_sell': 'SELL',
            'is_active': True,
        },
    )
    offer_buy = create_model_instance(
        'Offer',
        {
            'owner': buyer,
            'item': item,
            'number': 900,
            'price': '10.00',
            'buy_or_sell': 'BUY',
            'is_active': True,
        },
    )

    get_check_offers_task()
    inventory_sell = get_inventory_instance(inventory_sell.pk)
    assert inventory_sell.number == 1100


def test_send(get_django_mail):
    get_django_mail.send_mail('subject', 'body.', 'from@example.com', ['to@example.com'])
    assert len(get_django_mail.outbox) == 1


def test_send_again(get_send_email_task, get_django_mail):
    get_send_email_task('subject', 'body.', 'from@example.com', ['to@example.com'])
    out = get_django_mail.outbox
    assert len(get_django_mail.outbox) == 1
