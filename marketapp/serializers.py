from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from marketapp import models


class RegSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    car = serializers.HyperlinkedRelatedField(view_name='car-detail', read_only=True)

    class Meta:
        model = models.Comment
        fields = ['url', 'car', 'user', 'content', 'rating', 'date']
        read_only_fields = ['user', 'date']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['image']


class CarSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.username')
    brand = serializers.PrimaryKeyRelatedField(read_only=True, source='brand.name')
    comment_set = CommentSerializer(many=True, read_only=True)
    image_set = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Car
        fields = ['url', 'car_model', 'car_type', 'year', 'number_of_seats', 'colour', 'description', 'stock_count',
                  'price', 'brand', 'is_advertised', 'user', 'comment_set', 'image_set']
        read_only_fields = ['user', 'comment_set', 'image_set']


class PurchaseSerializer(serializers.ModelSerializer):
    stripe_token = serializers.CharField(required=True, write_only=True)
    stripe_email = serializers.EmailField(required=True, write_only=True)

    class Meta:
        model = models.Purchase
        fields = ['car', 'price', 'user', 'date', 'stripe_token', 'stripe_email']
        read_only_fields = ['price', 'user', 'date']

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context')
        if context:
            self.fields['car'].queryset = models.Car.objects.filter(stock_count__gt=0).exclude(
                user=context.pop('current_user'))
        self.fields['car'].allow_null = False
        super(PurchaseSerializer, self).__init__(*args, **kwargs)


class UserSerializer(serializers.ModelSerializer):
    purchase_set = PurchaseSerializer(many=True, read_only=True)
    car_set = CarSerializer(many=True, read_only=True)

    class Meta:
        model = models.User
        fields = ['url', 'image', 'username', 'email', 'first_name', 'last_name', 'car_set', 'purchase_set']
        read_only_fields = ['username', 'car_set', 'purchase_set']
