from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import PurchaseHistory

@receiver(post_save, sender=PurchaseHistory)
def send_purchase_email(sender, instance, created, **kwargs):
    """
    Sends an email to the user right after they make a new purchase.
    """
    if created:
        subject = 'You have a new purchase!'
        message = f'Your purchase tracking code is: {instance.id}'
        recipient_list = [instance.user.email]
        send_mail(subject, message, 'your_email@gmail.com', recipient_list)

