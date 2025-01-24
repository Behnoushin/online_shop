from django.contrib import admin
from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "total_amount", "status","address"]
    search_fields = ["user__username", "status"]
    list_filter = ["status"]
    ordering = ["-created_at"]
    list_per_page = 20
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'address')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "quantity"]
    search_fields = ["order__id", "product__title"]
    list_filter = ["order__status", "product"]
    ordering = ["order__id"]
    list_per_page = 20

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
