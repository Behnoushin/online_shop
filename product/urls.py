from django.urls import path
from .views import ProductList, ProductDetail, TopSellingProducts, PopularProductsView, CategoryList, CategoryDetail, CartView, CartProductsDetail, FavoriteListView, RemoveFromFavoriteList, RatingView, ReviewView,CouponListCreateView, CouponRetrieveUpdateDestroyView, ValidateCouponView , BrandList, BrandDetail, QuestionList, QuestionDetail, AnswerList, AnswerDetail

urlpatterns = [
    path("products/", ProductList.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetail.as_view(), name="product-detail"),
    path("top-selling-products/", TopSellingProducts.as_view(), name="top_selling_products"),
    path('popular-products/', PopularProductsView.as_view(), name='popular-products'),
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetail.as_view(), name="category-detail"),
    path("cart/", CartView.as_view(), name="cart-view"),
    path("cart/item/<int:pk>/", CartProductsDetail.as_view(), name="cart-item-detail"),
    path("favoritelist/", FavoriteListView.as_view(), name ="favorite-list"),
    path("favoritelist/remove/", RemoveFromFavoriteList.as_view(), name="favorite-list-remove"),
    path("rating/", RatingView.as_view(), name="rating-list"),
    path("review/", ReviewView.as_view(), name="review-list"),
    path("coupons/", CouponListCreateView.as_view(), name="coupon-list-create"),
    path("coupons/<int:pk>/", CouponRetrieveUpdateDestroyView.as_view(), name="coupon-detail"),
    path("validate-coupon/",ValidateCouponView.as_view(), name="validate-coupon"),
    path("brands/", BrandList.as_view(), name="brand-list"),
    path("brands/<int:pk>/", BrandDetail.as_view(), name="brand-detail"),
    path("questions/", QuestionList.as_view(), name="question-list"),
    path("questions/<int:pk>/", QuestionDetail.as_view(), name="question-detail"),
    path("answers/", AnswerList.as_view(), name="answer-list"),
    path("answers/<int:pk>/", AnswerDetail.as_view(), name="answer-detail"),
]