from django.db.models import TextChoices

class OrderStatusChoices(TextChoices):
    IN_TRANSIT = 'in_transit', 'In Transit'
    DELIVERED = 'delivered', 'Delivered'
    PENDING = 'pending', 'Pending'
