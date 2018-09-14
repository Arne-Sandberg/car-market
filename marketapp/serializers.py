from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from marketapp import models


class RegSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)


class ColourSerializer(serializers.Serializer):
    colour = serializers.CharField(read_only=True)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['image']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ['id', 'name', 'owner']


class PurchaseSerializer(serializers.ModelSerializer):
    stripe_token = serializers.CharField(required=True, write_only=True)
    stripe_email = serializers.EmailField(required=True, write_only=True)

    class Meta:
        model = models.Purchase
        depth = 1
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

    class Meta:
        depth = 1
        model = models.User
        fields = ['id', 'image', 'username', 'email', 'first_name', 'last_name', 'car_set', 'purchase_set',
                  'stripe_user_id', ]
        read_only_fields = ['username', 'car_set', 'purchase_set']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = ['id', 'car', 'user', 'content', 'rating', 'date']
        read_only_fields = ['user', 'date']


class CarSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    image_set = ImageSerializer(many=True, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Car
        fields = ['id', 'car_model', 'car_type', 'year', 'number_of_seats', 'colour', 'description', 'stock_count',
                  'price', 'brand', 'is_advertised', 'user', 'comment_set', 'image_set']
        read_only_fields = ['user', 'comment_set', 'image_set']
