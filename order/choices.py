from django.db.models import TextChoices


class OrderStatus(TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    CANCELED = 'canceled', 'Canceled'


class PaymentStatus(TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'