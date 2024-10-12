# Generated by Django 5.1.1 on 2024-10-11 17:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_management", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchasehistory",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="purchasehistory",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]