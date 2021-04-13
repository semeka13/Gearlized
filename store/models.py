from django.db import models
from auth.models import Account



class Product(models.Model):
    seller_id = models.ForeignKey(Account, related_name="seller", on_delete=models.CASCADE)
    buyer_id = models.ForeignKey(Account, related_name="buyer", on_delete=models.CASCADE)
    type = models.CharField(max_length=64)
    brand = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    size = models.CharField(max_length=64)
    condition = models.IntegerField()
    season = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    sold = models.BooleanField(default=False)
    publication_time = models.DateTimeField()
    extra_info = models.TextField()

    def __str__(self):
        return f"{self.model}, {self.seller_id}"


class Image(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    photo_n = models.IntegerField()
    photo = models.ImageField()

    def __str__(self):
        return self.photo