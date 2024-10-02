from django.contrib import admin
from .models import Product, Category, Cart
from usermanagement.models import CustomUser 

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


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "address"]
    search_fields = ["user__username", "address"]


class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "quantity", "purchase_date"]
    list_filter = ["purchase_date"]
    search_fields = ["user__username", "product__title"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
