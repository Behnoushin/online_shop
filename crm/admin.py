from django.contrib import admin
from info.admin import AboutUsAdmin, ContactUsAdmin, FAQAdmin
from product.admin import ProductAdmin, CategoryAdmin, CartAdmin, FavoriteListAdmin, RatingAdmin, ReviewAdmin
from user_management.admin import UserProfileAdmin, PurchaseHistoryAdmin
from info.models import AboutUs, ContactUs, FAQ
from product.models import Category, Product, Cart, FavoriteList, Rating, Review
from user_management.models import CustomUser, UserProfile, PurchaseHistory
from .models import AppAdmin

class AppAdminAdmin(admin.ModelAdmin):
    list_display = ['id', 'admin_username', 'created_at']
    search_fields = ['admin_user__username']

admin.site.register(AppAdmin, AppAdminAdmin)

