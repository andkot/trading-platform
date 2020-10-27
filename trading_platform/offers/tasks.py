from trading_platform.celery import app

from django.db.models import Min

from offers.models import (
    Offer,
    Trade,
)


@app.task
def check_offers():
    # get all offers
    offers = Offer.objects.all()

    # all offerings to sell
    offerings_to_sell = offers.filter(buy_or_sell='SELL')
    result = []
    # all offerings to buy
    offerings_to_buy = offers.filter(buy_or_sell='BUY')

    for of_to_buy in offerings_to_buy:
        if of_to_buy.is_active:
            # get list of available buy
            list_of_available_buys = offerings_to_sell.filter(item=of_to_buy.item,
                                                              number__gte=of_to_buy.number,
                                                              price__lte=of_to_buy.price,
                                                              is_active=True)

            # find minimal price
            buy_with_min_val = list_of_available_buys.aggregate(Min('price'))

            # if min price is found go to do trade
            if buy_with_min_val['price__min']:
                # get buy with minimal price
                buy = offerings_to_sell.annotate(Min('price')).order_by('price')[0]

                # if buy owner isn't offer to buy owner
                if buy.owner != of_to_buy.owner:
                    result.append((of_to_buy.id, buy.id))

                    Trade.objects.create(customer=of_to_buy.owner,
                                         seller=buy.owner,
                                         item=of_to_buy.item,
                                         number=of_to_buy.number,
                                         price=buy.price)

                    of_to_buy.is_active = False
                    buy.is_active = False
                    of_to_buy.save()
                    buy.save()
