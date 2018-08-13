from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    image = models.ImageField(null=True)


class Brand(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False, unique=True)
    owner = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Car(models.Model):
    car_model = models.CharField(max_length=70, blank=False, null=False)
    car_type = models.CharField(max_length=70)
    year = models.IntegerField()
    number_of_seats = models.IntegerField()
    colour = models.CharField(max_length=70)
    description = models.TextField()
    stock_count = models.IntegerField()
    price = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_advertised = models.BooleanField(default=False)

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
