from django.contrib import admin
from django.db.models import Avg
from .models import (
    Product, Category, Cart, CartProduct, FavoriteList, Rating, 
    Review, Coupon, Warranty, Brand, Question, Answer, RatingBrand,
    ReviewBrand, Comment, Report,
)

# -----------------------------------------------------------------------------
# CategoryAdmin
# -----------------------------------------------------------------------------
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "updated_at"]
    search_fields = ["name"]
    ordering = ["name"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at", "updated_at"]
    list_per_page = 20

# -----------------------------------------------------------------------------
# BrandAdmin
# -----------------------------------------------------------------------------
class BrandAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country", "created_at", "updated_at"]
    search_fields = ["name", "country"]
    ordering = ["name"]
    list_filter = ["country", "created_at"]
    readonly_fields = ["created_at", "updated_at"]
    list_per_page = 20

# -----------------------------------------------------------------------------
# WarrantyAdmin
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# ProductAdmin
# -----------------------------------------------------------------------------
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price", "category", "stock", "avg_rating"]
    search_fields = ["title", "description"]
    ordering = ["title"]
    list_filter = ["category", "price"]
    list_editable = ["stock", "price"]
    readonly_fields = ["avg_rating", "created_at", "updated_at"]
    list_per_page = 20

    def avg_rating(self, obj):
        avg = obj.ratings.aggregate(Avg('score'))['score__avg']
        return round(avg, 2) if avg else "No ratings yet"
    avg_rating.short_description = "Average Rating"


# -----------------------------------------------------------------------------
# CartAdmin
# -----------------------------------------------------------------------------
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "user", "total_price"]
    search_fields = ["products__title"]
    ordering = ["-created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["total_price", "created_at"]
    list_per_page = 20

# -----------------------------------------------------------------------------
# CartProductAdmin
# -----------------------------------------------------------------------------
class CartProductAdmin(admin.ModelAdmin):
    list_display = ["id", "cart", "product", "quantity"]
    search_fields = ["cart__id", "product__title"]
    ordering = ["cart", "product"]
    list_filter = ["cart", "product"]
    readonly_fields = ["created_at", "updated_at"]
    raw_id_fields = ("cart", "product")
    list_per_page = 20

# -----------------------------------------------------------------------------
# FavoriteListAdmin
# -----------------------------------------------------------------------------
class FavoriteListAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product_count"]
    search_fields = ["user__username"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at"]
    filter_horizontal = ("products",)
    list_per_page = 20

# -----------------------------------------------------------------------------
# RatingBrandAdmin
# -----------------------------------------------------------------------------
class RatingBrandAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "brand", "score", "status", "created_at"]
    search_fields = ["user__username", "brand__name"]
    ordering = ["-created_at"]
    list_filter = ["status", "created_at"]
    readonly_fields = ["created_at"]
    list_per_page = 20

    def score(self, obj):
        return obj.score
    score.short_description = "Score"

# -----------------------------------------------------------------------------
# ReviewBrandAdmin
# -----------------------------------------------------------------------------
class ReviewBrandAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "brand", "rate", "created_at"]
    search_fields = ["user__username", "brand__name"]
    ordering = ["-created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at"]
    list_per_page = 20

    def rate(self, obj):
        return obj.rate
    rate.short_description = "Rating"

# -----------------------------------------------------------------------------
# RatingAdmin
# -----------------------------------------------------------------------------
class RatingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "score", "created_at", "status"]
    search_fields = ["product__title"]
    ordering = ["-created_at"]
    list_filter = ["status", "created_at"]
    readonly_fields = ["created_at"]
    list_per_page = 20

# -----------------------------------------------------------------------------
# ReviewAdmin
# -----------------------------------------------------------------------------
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "created_at"]
    search_fields = ["product__title"]
    ordering = ["-created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at"]
    list_per_page = 20

# -----------------------------------------------------------------------------
# CouponAdmin
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# QuestionAdmin
# -----------------------------------------------------------------------------
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "text", "upvotes", "downvotes", "is_reported", "created_at", "updated_at"]
    search_fields = ["text", "user__username", "product__name"]
    ordering = ["created_at"]
    list_filter = ["is_reported", "created_at"]
    readonly_fields = ["created_at", "updated_at"]
    list_per_page = 20

# -----------------------------------------------------------------------------
# AnswerAdmin
# -----------------------------------------------------------------------------
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "user", "text", "is_approved", "upvotes", "downvotes", "created_at", "updated_at"]
    search_fields = ["text", "user__username", "question__id"]
    ordering = ["created_at"]
    list_filter = ["is_approved", "created_at"]
    readonly_fields = ["created_at", "updated_at"]
    list_per_page = 20

# -----------------------------------------------------------------------------
# CommentAdmin
# -----------------------------------------------------------------------------
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "answer", "text", "created_at"]
    search_fields = ["user__username", "answer__id", "text"]
    ordering = ["-created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at"]
    list_per_page = 20

# -----------------------------------------------------------------------------
# ReportAdmin
# -----------------------------------------------------------------------------
class ReportAdmin(admin.ModelAdmin):
    list_display = ["id", "reported_by", "content_type", "object_id", "reason", "created_at"]
    search_fields = ["reported_by__username", "content_type", "reason"]
    ordering = ["-created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at"]
    list_per_page = 20



admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Warranty, WarrantyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(FavoriteList, FavoriteListAdmin)
admin.site.register(RatingBrand, RatingBrandAdmin)
admin.site.register(ReviewBrand, ReviewBrandAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Report, ReportAdmin)
