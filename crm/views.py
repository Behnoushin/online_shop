from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer

class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class CategoryListUpdate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

