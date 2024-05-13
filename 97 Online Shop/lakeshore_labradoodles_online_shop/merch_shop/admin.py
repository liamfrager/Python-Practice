from django.contrib import admin
from .models import Color, Product, Variant

# Register your models here.
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(Variant)
