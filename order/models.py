from django.db import models
from product.models import Product
from utility.models import BaseModel
from user_management.models import CustomUser, Address, PurchaseHistory

class Order(BaseModel):
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="orders", null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.address.city}"

    def update_total_amount(self):
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_amount = total
        self.save()


class OrderItem(BaseModel):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} عدد از {self.product.title}"
    
    def get_total_price(self):
        return self.product.price * self.quantity
