# Generated by Django 5.1.1 on 2024-10-11 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AppAdmin",
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
                ("admin_username", models.CharField(max_length=150)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
