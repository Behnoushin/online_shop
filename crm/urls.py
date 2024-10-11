from django.urls import path
from .views import ProductUpdate

urlpatterns = [
    path("products/<int:pk>/update/", ProductUpdate.as_view(), name="product-update"),
]