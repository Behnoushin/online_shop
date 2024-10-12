from django.urls import path
from .views import ProductUpdate, CategoryListUpdate, AdminDashboardDataView, ProductDeleteView, UserProfileDeleteView

urlpatterns = [
    path("products/<int:pk>/update/", ProductUpdate.as_view(), name='product-update'),
    path("category/<int:pk>/update/", CategoryListUpdate.as_view(), name = 'category-update'),
    path("dashboard/", AdminDashboardDataView.as_view(), name='admin-dashboard-data'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('userprofiles/<int:pk>/delete/', UserProfileDeleteView.as_view(), name='userprofile-delete'),
]
