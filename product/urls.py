from django.urls import path
from .views import (
    ProductList, ProductDetail, TopSellingProducts, PopularProductsView, 
    CategoryList, CategoryDetail, CartView, CartProductsDetail, 
    FavoriteListView, RemoveFromFavoriteList, RatingView, ReviewView, 
    CouponListCreateView, CouponRetrieveUpdateDestroyView, ValidateCouponView, 
    WarrantyList, WarrantyDetail, BrandList, BrandDetail, ReviewEditDelete,
    QuestionList, QuestionDetail, AnswerList, AnswerDetail, SimilarProductsView,
    CommentList, ReportList, ProductsByBrand, FollowBrand, PopularBrandList, 
    RatingBrandListCreateView, RatingBrandEditDeleteView,
    ReviewBrandListCreateView, ReviewBrandEditDeleteView, 
)

urlpatterns = [
    
    # Category URLs
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetail.as_view(), name="category-detail"),
    
    # Brand URLs
    path("brands/", BrandList.as_view(), name="brand-list"),
    path("brands/<int:pk>/", BrandDetail.as_view(), name="brand-detail"),
    path("products/by-brand/<int:pk>/", ProductsByBrand.as_view(), name="products-by-brand"),
    path("follow/brand/<int:pk>/", FollowBrand.as_view(), name="follow-brand"),
    path("popular-brands/", PopularBrandList.as_view(), name="popular-brands"),
    
    # Warranty URLs
    path("warranties/", WarrantyList.as_view(), name="warranty-list"),
    path("warranties/<int:pk>/", WarrantyDetail.as_view(), name="warranty-detail"),
    
    # Product URLs
    path("products/", ProductList.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetail.as_view(), name="product-detail"),
    path("top-selling-products/", TopSellingProducts.as_view(), name="top_selling_products"),
    path("popular-products/", PopularProductsView.as_view(), name="popular-products"),
    path("similar-products/", SimilarProductsView.as_view(), name="similar-products"),

    # Cart URLs
    path("cart/", CartView.as_view(), name="cart-view"),
    path("cart/item/<int:pk>/", CartProductsDetail.as_view(), name="cart-item-detail"),

    # Favorite List URLs
    path("favoritelist/", FavoriteListView.as_view(), name="favorite-list"),
    path("favoritelist/remove/", RemoveFromFavoriteList.as_view(), name="favorite-list-remove"),
    
    # Rating and Review for Brand URLs
    path("rating/brand/", RatingBrandListCreateView.as_view(), name="brand-rating-list-create"),
    path("rating/brand/<int:brand_id>/", RatingBrandEditDeleteView.as_view(), name="brand-rating-edit-delete"),
    path("review/brand/", ReviewBrandListCreateView.as_view(), name="brand-review-list-create"),
    path("review/brand/<int:brand_id>/", ReviewBrandEditDeleteView.as_view(), name="brand-review-edit-delete"),

    # Rating and Review for Product URLs
    path("rating/", RatingView.as_view(), name="rating-list"),
    path("review/", ReviewView.as_view(), name="review-list"),
    path("review/<int:product_id>/", ReviewEditDelete.as_view(), name="review-edit-delete"),

    # Coupon URLs
    path("coupons/", CouponListCreateView.as_view(), name="coupon-list-create"),
    path("coupons/<int:pk>/", CouponRetrieveUpdateDestroyView.as_view(), name="coupon-detail"),
    path("validate-coupon/", ValidateCouponView.as_view(), name="validate-coupon"),

    # Question and Answer URLs
    path("questions/", QuestionList.as_view(), name="question-list"),
    path("questions/<int:pk>/", QuestionDetail.as_view(), name="question-detail"),
    path("questions/<int:question_id>/answers/", AnswerList.as_view(), name="answer-list"),
    path("answers/<int:answer_id>/comments/", CommentList.as_view(), name="comment-list"),
    path("answers/<int:pk>/", AnswerDetail.as_view(), name="answer-detail"),
    path("reports/", ReportList.as_view(), name="report-list"),

]