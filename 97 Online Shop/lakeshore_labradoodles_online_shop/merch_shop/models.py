from django.db import models

# Create your models here.


class ProductVariant(models.Model):
    variant_id = models.IntegerField()
    color_name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7)
    size = models.CharField(max_length=4)
