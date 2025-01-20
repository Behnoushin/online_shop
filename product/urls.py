from django.urls import path
from .views import ProductList, ProductDetail, CategoryList, CategoryDetail, CartView, CartProductsDetail, FavoriteListView, RemoveFromFavoriteList, RatingView, ReviewView,CouponListCreateView, CouponRetrieveUpdateDestroyView, BrandList, BrandDetail

urlpatterns = [
    path("products/", ProductList.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetail.as_view(), name="product-detail"),
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetail.as_view(), name="category-detail"),
    path("cart/", CartView.as_view(), name="cart-view"),
    path("cart/item/<int:pk>/", CartProductsDetail.as_view(), name="cart-item-detail"),
    path("favoritelist/", FavoriteListView.as_view(), name ="favorite-list"),
    path("favoritelist/remove/", RemoveFromFavoriteList.as_view(), name="favorite-list-remove"),
    path("rating/", RatingView.as_view(), name="rating-list"),
    path("review/", ReviewView.as_view(), name="review-list"),
    path('coupons/', CouponListCreateView.as_view(), name='coupon-list-create'),
    path('coupons/<int:pk>/', CouponRetrieveUpdateDestroyView.as_view(), name='coupon-detail'),
    path('brands/', BrandList.as_view(), name='brand-list'),
    path('brands/<int:pk>/', BrandDetail.as_view(), name='brand-detail'),
]