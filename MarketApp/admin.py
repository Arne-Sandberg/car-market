from django.contrib import admin
from .models import Brand, Car, Image


# Register your models here.

class ImageInline(admin.StackedInline):
    model = Image


class CarInline(admin.StackedInline):
    model = Car


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']
    inlines = [
        CarInline,
    ]


class CarAdmin(admin.ModelAdmin):
    list_display = ['car_model', 'car_type', 'year', 'registration_indicator', 'number_of_seats', 'colour',
                    'description', 'stock_count', 'price', 'brand']
    inlines = [
        ImageInline,
    ]


class ImageAdmin(admin.ModelAdmin):
    list_display = ['car', 'image']


admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)
