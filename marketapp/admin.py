from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from marketapp import models


class ImageInline(admin.StackedInline):
    model = models.Image


class BrandAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Brand._meta.fields if f.name != 'id']


class CarAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Car._meta.fields if f.name != 'id']
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
    list_display = [f.name for f in models.Comment._meta.fields if f.name != 'id']


class PurchaseAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Purchase._meta.fields if f.name != 'id']


admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Purchase, PurchaseAdmin)
admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Car, CarAdmin)
