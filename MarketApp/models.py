from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
