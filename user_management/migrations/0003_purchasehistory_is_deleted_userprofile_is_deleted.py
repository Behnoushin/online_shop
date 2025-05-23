# Generated by Django 5.1.1 on 2024-10-11 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_management", "0002_purchasehistory_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchasehistory",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]
