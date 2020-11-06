from trading_platform.celery import app

from django.db.models import Min

from offers.models import Offer, Trade, BuyOrSell


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, check_offers.s('asas'), name='add every 10 sec')


@app.task
def check_offers():
    # all offerings to sell
    offerings_to_sell = Offer.objects.filter(buy_or_sell=BuyOrSell.SELL.value)
    result = []
    # all offerings to buy
    offerings_to_buy = Offer.objects.filter(buy_or_sell=BuyOrSell.BUY.value)

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
