from django.contrib import admin
from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "total_amount", "status","address"]
    search_fields = ["user__username", "status"]
    list_filter = ["status"]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "quantity"]
    search_fields = ["order__id", "product__title"]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
