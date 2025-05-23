from django.db import models

class WarrantyStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    EXPIRED = 'expired', 'Expired'
    PENDING = 'pending', 'Pending'
    CANCELED = 'canceled', 'Canceled'


class RatingStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
