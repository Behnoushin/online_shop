# Generated by Django 5.1.1 on 2024-10-01 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0007_alter_contactus_phone_alter_faq_question_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="phone_number",
            field=models.CharField(max_length=15, null=True),
        ),
    ]
