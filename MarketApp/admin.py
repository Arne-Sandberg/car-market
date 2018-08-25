from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from MarketApp.models import Comment, Purchase
from .models import Brand, Car, Image, User


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


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'image', 'stripe_user_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ['car', 'user', 'content', 'rating', 'creation_date']


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'price', 'date']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)
