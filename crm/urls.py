from django.urls import path
from .views import ProductUpdate, CategoryListUpdate, AdminDashboardDataView

urlpatterns = [
    path("products/<int:pk>/update/", ProductUpdate.as_view(), name="product-update"),
    path("category/<int:pk>/update/", CategoryListUpdate.as_view, name = "category-update"),
    path("dashboard/", AdminDashboardDataView.as_view(), name='admin-dashboard-data'),
]