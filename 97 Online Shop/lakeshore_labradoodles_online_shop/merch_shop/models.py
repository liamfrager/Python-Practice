from django.db import models

# Create your models here.


class ShopProduct(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField(default=0)
    img = models.CharField(max_length=1000)
