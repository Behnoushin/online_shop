# -------------------   Django imports ------------------------
from django.db import models
from django.core.validators import MinValueValidator
# -------------------   Apps imports ------------------------
from product.models import Product
from utility.models import BaseModel
from user_management.models import CustomUser, Address
from .choices import OrderStatus, PaymentStatus

##################################################################################
#                             Order Model                                        #
##################################################################################

class Order(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="orders", null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING, db_index=True)
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending')
    shipping_date = models.DateTimeField(null=True, blank=True)
    tracking_number = models.CharField(max_length=50, null=True, blank=True)
    note = models.TextField(null=True, blank=True, help_text="Order Notes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'tracking_number'], name='unique_user_tracking')
        ]

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.address.city}"

    def update_total_amount(self):
        """
        Update total order amount 
        """
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_amount = total
        self.save()
        
    def mark_as_delivered(self):
        """
        Change status to delivered 
        """
        self.status = self.DELIVERED
        self.save()

    def mark_as_canceled(self):
        """ 
        Change status to Cancelled 
        """
        self.status = self.CANCELED
        self.save()

##################################################################################
#                           OrderItem Model                                      #
##################################################################################

class OrderItem(BaseModel):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} Number of {self.product.title}"
    
    def get_total_price(self):
        """ 
        Calculate the total price of each item 
        """
        return self.product.price * self.quantity
        
##################################################################################
#                             Payment Model                                      #
##################################################################################        
        
class Payment(BaseModel):
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)  
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    transaction_id = models.CharField(max_length=100, null=True, blank=True) 
    payment_date = models.DateTimeField(auto_now_add=True)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['transaction_id'], name='unique_transaction_id')
        ]

    def __str__(self):
        return f"Payment for Order {self.order.id} - Status: {self.payment_status}"

    def mark_as_paid(self):
        """ 
        Change status to paid 
        """
        self.payment_status = 'paid'
        self.save()