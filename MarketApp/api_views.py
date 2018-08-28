from django.utils import timezone
from rest_framework import generics, permissions
from MarketApp import models, serializers


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


class PurchaseList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer


