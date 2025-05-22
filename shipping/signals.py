from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Shipment

@receiver(post_save, sender=Shipment)
def shipment_post_save(sender, instance, created, **kwargs):
    if instance.order and instance.is_delivered:
        if instance.order.status != 'delivered':  
            instance.order.mark_as_delivered()
