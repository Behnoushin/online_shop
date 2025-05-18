from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import PurchaseHistory

@receiver(post_save, sender=PurchaseHistory)
def send_purchase_email(sender, instance, created, **kwargs):
    if created:
        subject = 'شما یک خرید جدید دارید!'
        message = f'کد پیگیری خرید شما: {instance.id}'
        recipient_list = [instance.user.email]
        send_mail(subject, message, 'your_email@gmail.com', recipient_list)

    