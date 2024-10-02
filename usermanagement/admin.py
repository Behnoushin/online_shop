from django.contrib import admin
from .models import UserProfile, PurchaseHistory, CustomUser

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "address"]
    search_fields = ["user__username", "address"]

class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "quantity", "purchase_date"]
    list_filter = ["purchase_date"]
    search_fields = ["user__username", "product__title"]

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PurchaseHistory, PurchaseHistoryAdmin)
admin.site.register(CustomUser)

