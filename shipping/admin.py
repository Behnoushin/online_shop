from django.contrib import admin
from .models import ShippingMethod, Shipment

class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "cost", "estimated_days", "available_from", "created_at"]
    search_fields = ["name", "cost"]
    ordering = ["-created_at"]
    list_filter = ["available_from", "cost"]
    list_per_page = 20

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "shipping_method", "tracking_number", "shipped_date", "delivered_date", "is_delivered", "estimated_delivery_date"]
    search_fields = ["order__id", "tracking_number", "order__user__username"]
    ordering = ["-shipped_date"]
    list_filter = ["is_delivered", "shipping_method", "shipped_date"]
    list_editable = ["is_delivered"]
    readonly_fields = ["tracking_number", "order"]
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('order', 'shipping_method')


admin.site.register(ShippingMethod, ShippingMethodAdmin)
admin.site.register(Shipment, ShipmentAdmin)
