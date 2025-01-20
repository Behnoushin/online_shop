from django.urls import path
from .views import get_exception_logs

urlpatterns = [
    path('api/errors/', get_exception_logs, name='get_exception_logs'),
]
