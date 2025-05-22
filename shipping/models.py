# -------------------   Django imports ------------------------
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
# -------------------   Apps imports ------------------------
from user_management.models import Address
from order.models import Order
from utility.models import BaseModel
from shipping.choices import OrderStatusChoices


##################################################################################
#                          ShippingMethod Model                                  #
##################################################################################
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
        return self.cost + (weight * 0.5) + (distance * 0.2)


##################################################################################
#                                Shipment Model                                  #
##################################################################################
    
class Shipment(BaseModel): 
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="shipment")
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True, blank=True)
    tracking_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    estimated_delivery_date = models.DateTimeField(null=True, blank=True)
    order_status = models.CharField(
        max_length=50,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING
    )
      
    def __str__(self):
        if self.order:
            return f"Shipment for Order {self.order.id} - {'Delivered' if self.is_delivered else 'In Transit'}"
        else:
            return "Shipment without Order"

    class Meta:
        ordering = ['-shipped_date']
       
    def clean(self):
        """
        Custom validation to ensure delivered_date is set if shipment is marked as delivered.
        """
        if self.is_delivered and not self.delivered_date:
            raise ValidationError("Delivered date must be set if shipment is marked as delivered.")
        super().clean()
    
    def save(self, *args, **kwargs):
        """
        Override save method to run clean validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)
                
    def mark_as_delivered(self):
        """
        Mark the shipment as delivered.
        """
        self.is_delivered = True
        self.order_status = OrderStatusChoices.DELIVERED
        self.save()
        if self.order:
            self.order.mark_as_delivered()

    def estimated_days_left(self):
        """
        Calculate and return the number of days left until the estimated delivery date.
        Returns None if estimated_delivery_date is not set.
        """
        if self.estimated_delivery_date:
            return (self.estimated_delivery_date - timezone.now()).days
        return None