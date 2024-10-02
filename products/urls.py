from django.urls import path
from .views import ProductList, ProductDetail, CategoryList, CategoryDetail, CartView, CartProductsDetail

urlpatterns = [
    path("products/", ProductList.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetail.as_view(), name="product-detail"),
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetail.as_view(), name="category-detail"),
    path("cart/", CartView.as_view(), name="cart-view"),
    path("cart/item/<int:pk>/", CartProductsDetail.as_view(), name="cart-item-detail"),
]
