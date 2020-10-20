from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from ..models import *
from django.contrib.auth.models import User


class CurrencySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ItemSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class WatchListSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = WatchList
        fields = '__all__'


class OfferSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class TradeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'


class InventorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class CreateUserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}