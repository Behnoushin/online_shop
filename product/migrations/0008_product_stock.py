# Generated by Django 5.1.1 on 2024-10-16 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0007_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="stock",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
