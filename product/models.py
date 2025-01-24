from django.db import models
from django.db.models import Avg
from django.conf import settings
from utility.models import BaseModel
from django.utils.timezone import now


class Category(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Brand(BaseModel): 
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=25000, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title + " - " + str(self.id) 
    

class Cart(BaseModel):
    products = models.ManyToManyField(Product)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True) 
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)


class CartProduct(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
class FavoriteList(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    product_count = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Favorite-list of {self.user.username}"
    
    def update_product_count(self):
        self.product_count = self.products.count()
        self.save()

    def add_product(self, product):
        if not self.products.filter(id=product.id).exists(): 
            self.products.add(product)
            self.update_product_count()

    def remove_product(self, product):
        if self.products.filter(id=product.id).exists(): 
            self.products.remove(product)
            self.update_product_count()

    def clear_products(self):
        self.products.clear()
        self.update_product_count()

    def has_product(self, product):
        return self.products.filter(id=product.id).exists()

    
class Rating(BaseModel):
    SCORE_CHOICES = [(i, str(i)) for i in range(6)]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(choices=SCORE_CHOICES, default=0)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved')], default='pending')
    
    def __str__(self):
        return f"{self.user.username}for {self.product.title} :{self.score}"

class Review(BaseModel):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey('user_management.CustomUser', on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.SmallIntegerField(null=True, blank=True)
    like = models.ManyToManyField('user_management.CustomUser', blank=True, related_name='liked_reviews')
    dislike = models.ManyToManyField('user_management.CustomUser', blank=True, related_name='disliked_reviews')
    parent_review = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='replies')
    
    def __str__(self):
        return f"{self.user.username} review for {self.product.title}"
    
class Coupon(BaseModel):
    code = models.CharField(max_length=15, unique=True)
    discount_value = models.FloatField()
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valid_from = models.DateTimeField(default=now)
    valid_until = models.DateTimeField()
    active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(blank=True, null=True)
    used_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.code
    
    def is_valid(self):
        if not self.active:
            return False
        if self.valid_from > now() or self.valid_until < now():
            return False
        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return False
        return True

    def calculate_discount(self, total_price):
        if not self.is_valid():
            return 0
        if self.min_purchase and total_price < self.min_purchase:
            return 0
        discount = total_price * (self.discount_value / 100) 
        if self.max_discount:
            discount = min(discount, self.max_discount)
        return discount
    
    
