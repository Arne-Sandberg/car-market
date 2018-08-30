from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from market_app import models


class RegSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['url', 'image', 'username', 'email', 'first_name', 'last_name', 'car_set', 'purchase_set']
        read_only_fields = ['username', 'car_set', 'purchase_set']


class CarSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)

    class Meta:
        model = models.Car
        fields = ['url', 'car_model', 'car_type', 'year', 'number_of_seats', 'colour', 'description', 'stock_count',
                  'price', 'brand', 'is_advertised', 'user', 'comment_set', 'image_set']
        read_only_fields = ['user', 'comment_set', 'image_set']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    car = serializers.HyperlinkedRelatedField(view_name='car-detail', read_only=True)

    class Meta:
        model = models.Comment
        fields = ['url', 'car', 'user', 'content', 'rating', 'date']
        read_only_fields = ['user', 'date']


class PurchaseSerializer(serializers.ModelSerializer):
    stripe_token = serializers.CharField(required=True)

    class Meta:
        model = models.Purchase
        fields = ['car', 'price', 'user', 'date', 'stripe_token']
        read_only_fields = ['price', 'user', 'date']

    def __init__(self, current_user, *args, **kwargs):
        super(PurchaseSerializer, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = models.Car.objects.filter(stock_count__gt=0).exclude(user=current_user)
        self.fields['car'].allow_null = False
