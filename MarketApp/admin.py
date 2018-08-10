from django.contrib import admin

from MarketApp.models import Profile
from .models import Brand, Car, Image


# Register your models here.

class ImageInline(admin.StackedInline):
    model = Image


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']


class CarAdmin(admin.ModelAdmin):
    list_display = ['car_model', 'car_type', 'year', 'number_of_seats', 'colour',
                    'description', 'stock_count', 'price', 'is_advertised', 'brand']
    inlines = [
        ImageInline,
    ]


admin.site.register(Profile)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)
