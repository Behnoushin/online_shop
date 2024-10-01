from django.urls import path
from .views import ProductList, ProductDetail, CategoryList, CategoryDetail, CartView, CartProductsDetail, AboutUsList, AboutUsDetail, ContactUsList, ContactUsDetail, FAQList, FAQDetail, UserRegistrationView, UserLoginView, UserProfileView, PurchaseHistoryView

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('cart/', CartView.as_view(), name='cart-view'),
    path('cart/item/<int:pk>/', CartProductsDetail.as_view(), name='cart-item-detail'),
    path('about/', AboutUsList.as_view(), name='about-list'),
    path('about/<int:pk>/', AboutUsDetail.as_view(), name='about-detail'),
    path('contact/', ContactUsList.as_view(), name='contact-list'),
    path('contact/<int:pk>/', ContactUsDetail.as_view(), name='contact-detail'),
    path('faq/', FAQList.as_view(), name='faq-list'),
    path('faq/<int:pk>/', FAQDetail.as_view(), name='faq-detail'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('purchase-history/', PurchaseHistoryView.as_view(), name='purchase-history'),
]