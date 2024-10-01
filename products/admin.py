from django.contrib import admin
from .models import Product, Category, Cart, AboutUs, ContactUs, FAQ, UserProfile, PurchaseHistory

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'price', 'category']
    search_fields = ['title']
    list_filter = ['category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields =['name']
    

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    list_filter = ['created_at']
    search_fields = ['products__title'] 
    
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'content']
    search_fields = ['content']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'phone', 'address']
    search_fields = ['email', 'phone']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'answer']
    search_fields = ['question']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'address', 'name']
    search_fields = ['user__username', 'address']
    
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'product', 'quantity', 'purchase_date']
    list_filter = ['purchase_date']
    search_fields = ['user__username', 'product__title'] 


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PurchaseHistory, PurchaseHistoryAdmin)