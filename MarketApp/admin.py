from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Brand, Car, Image, User


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


admin.site.register(User, UserAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)
