from django.contrib import admin
from .models import Product, Category, Cart

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category']
    search_fields = ['title']
    list_filter = ['category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields =['name']
    

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    list_filter = ['created_at']
    search_fields = ['products__title'] 

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)

