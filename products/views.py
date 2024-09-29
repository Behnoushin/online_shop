from .models import Product, Category, Cart, CartProduct
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartProductSerializer
from rest_framework import generics, status
from rest_framework.response import Response

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
class CartProductsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.quantity = request.data.get('quantity', instance.quantity)
        instance.save()
        return Response({"message": "به روز رسانی با موفقیت انحام شد "}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "محصول از سبد خرید حذف شد"}, status=status.HTTP_204_NO_CONTENT)
