from django.contrib import admin

# Register your models here.
from store.models import Products, User, Image

admin.site.register(Products)
admin.site.register(User)
admin.site.register(Image)
