from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False)
    owner = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Car(models.Model):
    REG_INDICATOR = (('N', 'New'), ('U', 'Used vehicle'), ('R', 'Re-registrations'), ('S', 'Scratch-built'))

    car_model = models.CharField(max_length=70, blank=False, null=False)
    car_type = models.CharField(max_length=70)
    year = models.IntegerField()
    registration_indicator = models.CharField(max_length=20, choices=REG_INDICATOR, default='N')
    number_of_seats = models.IntegerField()
    colour = models.CharField(max_length=70)
    description = models.TextField(max_length=256)
    stock_count = models.IntegerField()
    price = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_advertised = models.BooleanField(default=False)

    def __str__(self):
        return str(self.brand) + ' - ' + self.car_model + ' ' + str(self.year) + ' - ' + self.car_type


class Image(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    image = models.ImageField()
