from rest_framework import generics
from .models import AppAdmin
from .serializers import AppAdminSerializer
from rest_framework.permissions import IsAuthenticated

class AppAdminListCreateView(generics.ListCreateAPIView):
    queryset = AppAdmin.objects.all()
    serializer_class = AppAdminSerializer
    permission_classes = [IsAuthenticated]
    
class AppAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppAdmin.objects.all()
    serializer_class = AppAdminSerializer
    permission_classes = [IsAuthenticated]