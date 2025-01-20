from rest_framework import generics
from .models import ExceptionLog
from .serializers import ExceptionLogSerializer

class ExceptionLogListView(generics.ListAPIView):
    queryset = ExceptionLog.objects.all()
    serializer_class = ExceptionLogSerializer
