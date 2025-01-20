from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product"
    
    def ready(self):
        from django.db.models.signals import pre_migrate
        from django.db import models
        from django.apps import apps

        Product = apps.get_model('product', 'Product')
        CustomUser = apps.get_model('user_management', 'CustomUser')