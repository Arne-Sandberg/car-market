from rest_framework import serializers
from MarketApp import models


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.fields['username'].read_only = True
        self.fields['car_set'].read_only = True
        self.fields['purchase_set'].read_only = True

    class Meta:
        model = models.User
        fields = ('url', 'image', 'username', 'email', 'first_name', 'last_name', 'car_set', 'purchase_set')


class CarSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Car
        fields = ('url', 'car_model', 'car_type', 'year', 'number_of_seats', 'colour', 'description', 'stock_count',
                  'price', 'brand', 'is_advertised', 'user', 'comment_set', 'image_set')

    def __init__(self, *args, **kwargs):
        super(CarSerializer, self).__init__(*args, **kwargs)
        self.fields['comment_set'].read_only = True
        self.fields['image_set'].read_only = True


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Comment
        fields = ('url', 'car', 'user', 'content', 'rating', 'date')

    def __init__(self, *args, **kwargs):
        super(CommentSerializer, self).__init__(*args, **kwargs)
        self.fields['date'].read_only = True
