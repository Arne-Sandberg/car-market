import webcolors
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    image = models.ImageField(null=True, blank=True)
    stripe_user_id = models.CharField(max_length=256, blank=True, null=True)


class Brand(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False, unique=True)
    owner = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Car(models.Model):
    COLOUR_CHOICES = [(i, i) for i in webcolors.HTML4_HEX_TO_NAMES.values()]

    car_model = models.CharField(max_length=70)
    car_type = models.CharField(max_length=70)
    year = models.IntegerField()
    number_of_seats = models.IntegerField()
    colour = models.CharField(choices=COLOUR_CHOICES, max_length=70)
    description = models.TextField(null=True, blank=True)
    stock_count = models.IntegerField(default=1)
    price = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_advertised = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.brand} - {self.car_model} {self.year} - {self.car_type}'


class Image(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    image = models.ImageField()


class Comment(models.Model):
    content = models.TextField()
    rating = models.IntegerField(default=1)
    creation_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)


class Purchase(models.Model):
    date = models.DateTimeField(default=timezone.now)
    price = models.IntegerField()
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
