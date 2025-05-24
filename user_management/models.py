# -------------------   Django imports ------------------------
from django.db import models
from django.contrib.auth.models import AbstractUser
# -------------------   Apps imports ------------------------
from product.models import Product
from utility.models import BaseModel


##################################################################################
#                        CustomUser Model                                        #
##################################################################################

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, help_text="Age must be at least 13 years old.")
    fixed_phone = models.CharField(max_length=15, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "Custom User" 
        verbose_name_plural = "Custom Users"
        ordering = ['username']
        
##################################################################################
#                           Address Model                                        #
##################################################################################

class Address(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street}, {self.city} ({'Default' if self.is_default else 'Other'})"
    
    class Meta:
        verbose_name = "User Address"
        verbose_name_plural = "User Addresses"
        ordering = ['city', 'street']
        constraints = [
            models.UniqueConstraint(fields=['user'], condition=models.Q(is_default=True), name='unique_default_address_per_user')
        ]
        
##################################################################################
#                           UserProfile Model                                    #
##################################################################################

class UserProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    addresses = models.ManyToManyField('Address', blank=True, related_name='user_profiles')
    
    def get_default_address(self):
        return self.addresses.filter(is_default=True).first()
    
    def __str__(self):
        return self.user.username

##################################################################################
#                           PurchaseHistory Model                                #
##################################################################################

class PurchaseHistory(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="purchase_histories")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchases")
    quantity = models.PositiveIntegerField(default=1, help_text="The number of products purchased.")
    purchase_date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchase_history", default=None, help_text="Address where the product will be delivered.")
    is_delivered = models.BooleanField(default=False, help_text="Whether the product is delivered.")

    
    class Meta:
        ordering = ["-purchase_date"]
    
    def __str__(self):
        return f"User: {self.user.username}, Product: {self.product.title}, Address: {self.address.street if self.address else 'No Address'}"
    
    def total_cost(self):
        return self.quantity * self.product.price
