from django.db import models


class Account(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    registration_time = models.DateTimeField()
    email = models.EmailField(max_length=254, default="default.email@gmail.com")

    def __str__(self):
        return self.email

