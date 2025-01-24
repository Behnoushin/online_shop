from django.urls import path
from .views import OrderView , OrderDetailView, OrderItemView

urlpatterns = [
    path("orders/", OrderView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:order_id>/items/", OrderItemView.as_view(), name="order-item-list"),
]
