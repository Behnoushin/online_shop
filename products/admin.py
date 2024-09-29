from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category']
    search_fields = ['title']
    list_filter = ['category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields =['name']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
