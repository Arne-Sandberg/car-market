from rest_framework import serializers

from MarketApp import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['url', 'image', 'username', 'email', 'first_name', 'last_name', 'car_set', 'purchase_set']
        read_only_fields = ['username', 'car_set', 'purchase_set']


class CarSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Car
        fields = ['url', 'car_model', 'car_type', 'year', 'number_of_seats', 'colour', 'description', 'stock_count',
                  'price', 'brand', 'is_advertised', 'user', 'comment_set', 'image_set']
        read_only_fields = ['comment_set', 'image_set']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Comment
        fields = ['url', 'car', 'user', 'content', 'rating', 'date']
        read_only_fields = ['date']


class PurchaseSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    card_number = serializers.IntegerField(required=True)
    expire_month = serializers.IntegerField(required=True, min_value=1, max_value=12)
    expire_year = serializers.IntegerField(required=True, min_value=1)
    cvc = serializers.IntegerField(required=True)

    class Meta:
        model = models.Purchase
        fields = ['car', 'price', 'user', 'date', 'email', 'card_number', 'expire_month', 'expire_year', 'cvc']
        read_only_fields = ['price', 'user', 'date']
        write_only_fields = ['email', 'card_number', 'expire_month', 'expire_year', 'cvc']

    def __init__(self, current_user, *args, **kwargs):
        super(PurchaseSerializer, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = models.Car.objects.filter(stock_count__gt=0).exclude(user=current_user)
        self.fields['car'].allow_null = False
