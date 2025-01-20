# Generated by Django 5.1.1 on 2025-01-20 15:58

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0008_product_stock"),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=100)),
                ("image", models.CharField(blank=True, max_length=25000, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="product",
            name="brand",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="product.brand",
            ),
        ),
    ]
