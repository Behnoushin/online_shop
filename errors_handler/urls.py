from django.urls import path
from .views import ExceptionLogListView

urlpatterns = [
    path('api/errors/', ExceptionLogListView.as_view(), name='get_exception_logs'),
]
