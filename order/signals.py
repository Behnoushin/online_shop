from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import OrderItem
from product.models import Product

@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total_amount(sender, instance, **kwargs):
    order = instance.order
    total = sum(item.get_total_price() for item in order.items.all())
    order.total_amount = total
    order.save()

@receiver(post_save, sender=OrderItem)
def check_low_stock(sender, instance, **kwargs):
    product = instance.product
    product.stock -= instance.quantity
    product.save()
    
    threshold = 5
    if product.stock < threshold:
        print(" Low Stock Alert:")
        print(f"Product Name: {product.title}")
        print(f"Current Stock: {product.stock}")
        print(f"Alert Threshold: {threshold}")
        print(f"Product ID: {product.id}")
