from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Rating, Product

@receiver(post_save, sender=Rating)
# Triggered when a new Rating is created
def notify_new_rating(sender, instance, create, **kwargs):
    if create:
        print(f"New score for {instance.product.title} registered by {instance.user.username}!")
        
        
        
@receiver(post_save, sender=Product)
# Triggered when a Product is created or updated
def notify_product_saved(sender, instance, create, **kwargs):
    if create:
        print (f"New product created: {instance.title}")
    else:
        print(f"Product edited: {instance.title}")
        

@receiver(post_delete, sender=Product)
# Triggered when a Product is deleted
def notify_product_deleted(sender, instance, **kwargs):
    print(f" Product deleted: {instance.title}")