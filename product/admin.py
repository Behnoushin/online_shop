from django.contrib import admin
from django.db.models import Avg
from .models import Product, Category, Cart, FavoriteList, Rating, Review, Coupon, Warranty, Brand, Question, Answer

class BrandAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country", "created_at", "updated_at"]
    search_fields = ["name", "country"]
    ordering = ["name"]
    list_filter = ["country", "created_at"]
    readonly_fields = ["created_at", "updated_at"]
    list_per_page = 20
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price", "category", "stock", "avg_rating"]
    search_fields = ["title", "description"]
    ordering = ["title"]
    list_filter = ["category", "price"]
    list_editable = ["stock","price"]
    readonly_fields = ["avg_rating", "created_at", "updated_at"]
    list_per_page = 20
    
    def avg_rating(self, obj):
        avg = obj.ratings.aggregate(Avg('score'))['score__avg']
        return round(avg, 2) if avg else "No ratings yet"
    avg_rating.short_description = "Average Rating"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "updated_at"]
    search_fields = ["name"]
    ordering = ["name"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at", "updated_at"]
    list_per_page = 20


class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "user", "total_price"]
    search_fields = ["products__title"]
    ordering = ["-created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["total_price", "created_at"]
    list_per_page = 20


class FavoriteListAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product_count"]
    search_fields = ["user__username"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at"]
    filter_horizontal = ("products",)
    list_per_page = 20
   
    
class RatingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "score", "created_at","status"]
    search_fields =["product__title"]
    ordering = ["-created_at"]
    list_filter = ["status", "created_at"]
    readonly_fields = ["created_at"]
    list_per_page = 20
  
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "created_at"]
    search_fields = ["product__title"]
    ordering = ["-created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at"]
    list_per_page = 20
   
    
class CouponAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "discount_value", "valid_until", "active", "is_valid_now"]
    search_fields = ["code"]
    ordering = ["-valid_until"]
    list_filter = ["active", "valid_until"]
    readonly_fields = ["used_count"]
    list_per_page = 20
    
    def is_valid_now(self, obj):
        return obj.is_valid()
    is_valid_now.short_description = "Valid Now"
    is_valid_now.boolean = True
    
class WarrantyAdmin(admin.ModelAdmin):
    list_display = ["product", "start_date", "end_date", "status", "description"]
    search_fields = ["product__name", "description"]
    ordering = ["-start_date"]
    list_filter = ["status", "start_date", "end_date"]
    readonly_fields = ["start_date", "end_date", "status"]
    list_per_page = 20

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("product")
        return queryset
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "text", "upvotes", "downvotes", "is_reported", "created_at", "updated_at"]
    search_fields = ["text", "user__username", "product__name"]
    ordering = ["created_at"]
    list_filter = ["is_reported", "created_at"]
    readonly_fields = ["created_at", "updated_at"]
    list_per_page = 20
    

class AnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "user", "text", "is_approved", "upvotes", "downvotes", "created_at", "updated_at"]
    search_fields = ["text", "user__username", "question__id"]
    ordering = ["created_at"]
    list_filter = ["is_approved", "created_at"]
    readonly_fields = ["created_at", "updated_at"]
    list_per_page = 20

admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(FavoriteList, FavoriteListAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Warranty, WarrantyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
