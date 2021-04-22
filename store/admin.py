from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from store.models import Products, User, Image


# Define a new User admin
class UserAdmin(admin.ModelAdmin):
    pass


class ProductsAdmin(admin.ModelAdmin):
    pass


class ImageAdmin(admin.ModelAdmin):
    pass


# Re-register UserAdmin
admin.site.register(Products, ProductsAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(User, UserAdmin)
