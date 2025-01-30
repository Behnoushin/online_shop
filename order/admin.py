from django.contrib import admin
from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "total_amount", "status", "address", "created_at"]
    search_fields = ["user__username", "status"]
    ordering = ["-created_at"]
    list_filter = ["status", "created_at", "updated_at"]
    list_editable = ["status"]
    read_only_fields = ["total_amount", "user", "address"]
    list_per_page = 20
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'address')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "quantity", "created_at"]
    search_fields = ["order__id", "product__title"]
    ordering = ["order__id"]
    list_filter = ["order__status", "product", "created_at"]
    list_editable = ["quantity"]
    read_only_fields = ["order", "product"]
    list_per_page = 20

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
