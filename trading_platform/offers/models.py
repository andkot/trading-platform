from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from enum import Enum


class BuyOrSell(Enum):
    BUY = 'BUY'
    SELL = 'SELL'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


# User = settings.AUTH_USER_MODEL


class Currency(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=128, unique=True)


class Item(models.Model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1)])


class WatchList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class Offer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1)])
    buy_or_sell = models.CharField(max_length=10, choices=BuyOrSell.choices())
    is_active = models.BooleanField(default=True)


class Trade(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(null=False, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1)])


class Inventory(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
