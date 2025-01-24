from django.contrib import admin
from .models import Product, Category, Cart, FavoriteList, Rating, Review, Coupon, Brand

class BrandAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country", "created_at", "updated_at"]
    list_filter = ["country", "created_at"]
    search_fields = ["name", "country"]

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
    list_display = ["id", "user", "product_count"]
    search_fields = ["user__username"]
    filter_horizontal = ("products",)
    
class RatingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "score", "created_at","status"]
    search_fields =["product__title"]
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "created_at"]
    search_fields = ["product__title"]
    
class CouponAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "discount_value", "valid_until", "active", "is_valid_now"]
    list_filter = ["active", "valid_until"]
    search_fields = ["code"]
    readonly_fields = ["used_count"]
    
    def is_valid_now(self, obj):
        return obj.is_valid()
    is_valid_now.short_description = "Valid Now"
    is_valid_now.boolean = True
    
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(FavoriteList, FavoriteListAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Coupon, CouponAdmin)

