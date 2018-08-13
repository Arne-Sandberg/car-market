from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from MarketApp.models import Comment
from .models import Brand, Car, Image, User
from django.utils.translation import ugettext_lazy as _


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
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'image')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ['car', 'user', 'content', 'rating', 'creation_date']


admin.site.register(Comment, CommentAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)
