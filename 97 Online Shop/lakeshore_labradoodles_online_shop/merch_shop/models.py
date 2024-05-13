from django.db import models

# Create your models here.


class Color(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7)


class Product(models.Model):
    product_id = models.IntegerField()
    colors = models.ManyToManyField(Color)
    size = models.CharField(max_length=4)


class Variant(models.Model):
    variant_id = models.IntegerField()
    stripe_price_id = models.CharField(max_length=30)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.CharField(max_length=4)
