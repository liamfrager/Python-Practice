# Generated by Django 4.2.11 on 2024-05-14 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merch_shop', '0016_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.URLField(default=''),
        ),
    ]