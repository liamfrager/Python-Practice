from django.db import models

# Create your models here.


class Color(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7)


class Price(models.Model):
    id = models.CharField(primary_key=True, max_length=30)  # Stripe price ID
    value = models.DecimalField(decimal_places=2, max_digits=5)  # Price in USD


class Product(models.Model):
    SIZE_OPTIONS = [
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("2XL", "2XL"),
        ("3XL", "3XL"),
        ("4XL", "4XL"),
        ("5XL", "5XL"),
    ]
    id = models.IntegerField(primary_key=True)  # Printful product ID
    colors = models.ManyToManyField(Color)
    sizes = models.CharField(max_length=4, choices=SIZE_OPTIONS)


class Variant(models.Model):
    id = models.IntegerField(primary_key=True)  # Printful variant ID
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.CharField(max_length=4)
