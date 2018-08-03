from django.contrib import admin
from .models import Brand, Car


# Register your models here.


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']


class CarAdmin(admin.ModelAdmin):
    list_display = ['image_url', 'car_model', 'car_type', 'year', 'registration_indicator', 'number_of_seats', 'colour',
                    'description', 'brand']


admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)
