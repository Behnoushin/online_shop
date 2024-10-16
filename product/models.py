from django.db import models
from django.conf import settings
from utility.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title


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
    
    def __str__(self):
        return f"Favorite-list of {self.user.username}"
    
class Rating(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}for {self.product.title} :{self.score}"

class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    
    def __str__(self):
        return f"{self.user.username} review for {self.product.title}"
    
class Coupon(BaseModel):
    code = models.CharField(max_length=15, unique=True)
    discount = models.FloatField()
    valid_until = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code