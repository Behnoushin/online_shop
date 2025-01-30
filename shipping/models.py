from django.db import models
from user_management.models import Address
from order.models import Order
from utility.models import BaseModel
from django.utils import timezone

class ShippingMethod(BaseModel):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.PositiveIntegerField()
    available_from = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.cost} USD ({self.estimated_days} days)"
    
    class Meta:
        ordering = ['name']
        
    def calculate_shipping_cost(self, weight, distance):
        """
        Calculate shipping cost based on weight and distance.
        """
        base_cost = self.cost
        additional_cost = (weight * 0.5) + (distance * 0.2)
        return base_cost + additional_cost
    
    
class Shipment(BaseModel):
    ORDER_STATUS_CHOICES = [
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('pending', 'Pending'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipment")
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True, blank=True)
    tracking_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    estimated_delivery_date = models.DateTimeField(null=True, blank=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='pending')

      
    def __str__(self):
        return f"Shipment for Order {self.order.id} - {'Delivered' if self.is_delivered else 'In Transit'}"

    class Meta:
        ordering = ['-shipped_date']
        
    def mark_as_delivered(self):
        """
        Mark the shipment as delivered.
        """
        self.is_delivered = True
        self.order_status = 'delivered'
        self.save()

    def estimated_days_left(self):
        """
        Calculate remaining days for estimated delivery.
        """
        if self.estimated_delivery_date:
            return (self.estimated_delivery_date - timezone.now()).days
        return None