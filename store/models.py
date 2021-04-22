import os
from datetime import datetime

import django
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    registration_time = models.DateTimeField(default=django.utils.timezone.now())
    phone_number = models.CharField(max_length=15, default="8228228228")
    email = models.EmailField(max_length=254, default="default.email@gmail.com")
    country = CountryField(default="Russia")
    city = models.CharField(max_length=256, default="Vladivostok")
    is_active = models.BooleanField(default=True)



    def __str__(self):
        return f"{self.username}-{self.email}"


class Products(models.Model):
    seller = models.ForeignKey(User, related_name="seller", on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name="buyer", on_delete=models.CASCADE)
    TYPES_OF_EQUIPMENT = [("snb", 'snowboard'), ("ski", 'ski'), ("bike", 'bike')]
    type = models.CharField(choices=TYPES_OF_EQUIPMENT, help_text='Type of equipment', blank=False, max_length=64)
    brand = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    size = models.CharField(max_length=64)
    condition = models.IntegerField()
    season = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    sold = models.BooleanField(default=False)
    publication_time = models.DateTimeField()
    extra_info = models.TextField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.model}, {self.seller}"


class Image(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='./static/product_pictures', blank=False)

    def __str__(self):
        return f"image {self.product}"


