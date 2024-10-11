from django.contrib import admin
from .models import Product, Category, Cart, FavoriteList, Rating, Review

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price", "category"]
    search_fields = ["title"]
    list_filter = ["category"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "user"]
    list_filter = ["created_at"]
    search_fields = ["products__title"]

class FavoriteListAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    search_fields = ["user__username"]
    
class RatingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "score", "created_at"]
    search_fields =["product__title"]
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "created_at"]
    search_fields = ["product__title"]
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(FavoriteList, FavoriteListAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Review, ReviewAdmin)
