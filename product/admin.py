from django.contrib import admin
from .models import Product, Category, Cart, FavoriteList, Rating, Review, Coupon

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price", "category", "stock"]
    search_fields = ["title", "description"]
    list_filter = ["category", "price"]
    list_editable = ["stock","price"]
    

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
    
class CouponAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "discount", "valid_until"]
    search_fields = ["code"]
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(FavoriteList, FavoriteListAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Coupon, CouponAdmin)

