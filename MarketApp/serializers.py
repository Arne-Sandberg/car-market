from rest_framework import serializers

from MarketApp import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('url', 'username', 'email', 'first_name', 'last_name')


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Car
        exclude = ('description',)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        exclude = ('creation_date',)


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Purchase
        exclude = ('date',)
