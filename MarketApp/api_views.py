from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from MarketApp import models, serializers
from MarketApp.utils import create_charge


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


class CarDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer


class UserList(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class MyDetail(generics.RetrieveUpdateAPIView):
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
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
        return serializer_class(self.request.user, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        result = create_charge(request, request.data['car'], request.data['stripe_token'])
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) if result else Response(
            {"detail": "Your card was declined"}, status=status.HTTP_406_NOT_ACCEPTABLE)
