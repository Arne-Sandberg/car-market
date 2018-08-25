import webcolors
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.utils import timezone


class User(AbstractUser):
    image = models.ImageField(null=True, blank=True)
    stripe_user_id = models.CharField(max_length=256, blank=True, null=True)


class Brand(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False, unique=True)
    owner = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class CarManager(models.Manager):
    def search_cars(self, search_content):
        return self.get_queryset().filter(
            Q(car_model__icontains=search_content) | Q(description__icontains=search_content) | Q(
                brand__name__icontains=search_content) | Q(colour__icontains=search_content))

    def advertisement(self):
        return self.get_queryset().filter(is_advertised=True)

    def filter_cars(self, data, brand_id, search_content=''):
        if search_content:
            cars = self.search_cars(search_content)
        else:
            cars = self.get_queryset()
        if brand_id:
            cars = cars.filter(brand_id=brand_id)
        if data['colour'] != 'any colour':
            cars = cars.filter(colour=data['colour'])
        if data['in_stock_only'] == 'true':
            cars = cars.filter(stock_count__gt=0)
            print()
        cars = cars.filter(year__lte=data['max_year'], year__gte=data['min_year'],
                           number_of_seats=data['number_of_seats'], price__gte=data['min_price'],
                           price__lte=data['max_price'])
        return cars


class Car(models.Model):
    COLOUR_CHOICES = [(i, i) for i in webcolors.HTML4_HEX_TO_NAMES.values()]

    car_model = models.CharField(max_length=70)
    car_type = models.CharField(max_length=70)
    year = models.IntegerField()
    number_of_seats = models.IntegerField(default=4)
    colour = models.CharField(choices=COLOUR_CHOICES, max_length=70)
    description = models.TextField(null=True, blank=True)
    stock_count = models.IntegerField(default=1)
    price = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_advertised = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    objects = CarManager()

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
