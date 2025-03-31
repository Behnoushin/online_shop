from django.urls import path
from .views import (
    OrderView , OrderDetailView, OrderItemView,
    PaymentListCreateView, PaymentDetailView
    )

urlpatterns = [
    # Order URLs
    path("orders/", OrderView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    
    # OrderItem URLs
    path("orders/<int:order_id>/items/", OrderItemView.as_view(), name="order-item-list"),
    
    # Payment URLs
    path("payments/", PaymentListCreateView.as_view(), name="payment-list-create"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),

]
