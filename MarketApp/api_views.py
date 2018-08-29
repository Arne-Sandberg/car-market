import stripe
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from Market import settings
from MarketApp import models, serializers, tasks


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class CarList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CarDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer


class UserList(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class MyDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class AdvertisementList(generics.ListAPIView):
    queryset = models.Car.objects.filter(is_advertised=True)
    serializer_class = serializers.CarSerializer


class CommentList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_update(self, serializer):
        serializer.save(date=timezone.now())


class Checkout(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PurchaseSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['current_user'] = self.request.user
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        data = self.request.data
        car = models.Car.objects.get(id=data['car'])
        car.stock_count -= 1
        try:
            token = stripe.Token.create(
                card={
                    "number": data['card_number'],
                    "exp_month": data['expire_month'],
                    "exp_year": data['expire_year'],
                    "cvc": data['cvc']
                },
            ).get('id')
            if car.user:
                stripe.Charge.create(
                    amount=int(car.price * 92.9 + 30),
                    currency="usd",
                    source=token,
                    description=f"{car} {car.colour} was sold to {self.request.user}",
                    application_fee=int(car.price * 7.1 - 30),
                    stripe_account=car.user.stripe_user_id,
                )
            else:
                stripe.Charge.create(
                    amount=car.price * 100,
                    currency="usd",
                    source=token,
                    description=f"{car} {car.colour} was sold to {self.request.user}",
                )
        except stripe.error.CardError:
            return Response({"detail": "Your card was declined"}, status=status.HTTP_406_NOT_ACCEPTABLE, )
        else:
            reciever = data['email']
            msg = f'Thank you, for purchasing {car}.\nThe information about purchase would be available at:\n' + \
                  f'http://{get_current_site(self.request).domain}/accounts/profile/{self.request.user}'
            tasks.send_message(reciever, 'Car purchasing', msg)
            models.Purchase.objects.create(user=self.request.user, price=car.price, date=timezone.now(), car=car)
            car.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
