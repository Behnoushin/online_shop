from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import OrderItem

@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total_amount(sender, instance, **kwargs):
    order = instance.order
    total = sum(item.get_total_price() for item in order.items.all())
    order.total_amount = total
    order.save()

