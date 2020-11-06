from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from django.contrib.auth.models import User

from offers.models import (
    Currency,
    Item,
    WatchList,
    Offer,
    Trade,
    Inventory,
)


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class WatchListSerializer(ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.pk')

    class Meta:
        model = WatchList
        fields = '__all__'

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super(WatchListSerializer, self).create(validated_data)


class OfferSerializer(ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.pk')

    class Meta:
        model = Offer
        fields = '__all__'

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super(OfferSerializer, self).create(validated_data)


class TradeSerializer(ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'


class InventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class CreateUserSerializer(ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'repeat_password')
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        repeat_password = validated_data.pop('repeat_password')
        password = validated_data.pop('password')
        if repeat_password != password:
            raise serializers.ValidationError("Passwords do not match")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(ModelSerializer):
    is_superuser = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['username', 'is_superuser', 'pk']

# class UserLoginSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'password')
