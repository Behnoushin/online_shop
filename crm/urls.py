from django.urls import path
from .views import AppAdminListCreateView, AppAdminDetailView

urlpatterns = [
    path('admins/', AppAdminListCreateView.as_view(), name='admin-list-create'),
    path('admins/<int:pk>/', AppAdminDetailView.as_view(), name='admin-detail'),
]