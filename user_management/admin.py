from django.contrib import admin
from .models import UserProfile, PurchaseHistory, CustomUser, Address

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "get_default_address"]
    search_fields = ["user__username"]
    ordering = ["user__username"]
    list_filter = ["user__username"]
    readonly_fields = ["user"]
    
    def get_default_address(self, obj):
        default_address = obj.get_default_address()
        return default_address.street if default_address else "No Default Address"
    get_default_address.short_description = "Default Address"

class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "quantity", "purchase_date", "is_delivered"]
    search_fields = ["user__username", "product__title"]
    ordering = ["-purchase_date"]
    list_filter = ["purchase_date", "is_delivered"]
    list_editable = ["is_delivered"]
    readonly_fields = ["user", "product", "purchase_date"]
    date_hierarchy = "purchase_date"


admin.site.register(CustomUser)
admin.site.register(Address)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PurchaseHistory, PurchaseHistoryAdmin)
