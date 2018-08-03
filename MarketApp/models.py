from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False)
    owner = models.CharField(max_length=70)

    def __str__(self):
        return self.name + ' - ' + self.owner


class Car(models.Model):
    image_url = models.URLField()
    car_model = models.CharField(max_length=70, blank=False, null=False)
    car_type = models.CharField(max_length=70)
    year = models.IntegerField()
    registration_indicator = models.CharField(max_length=70)
    number_of_seats = models.IntegerField()
    colour = models.CharField(max_length=70)
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

