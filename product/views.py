from .models import Product, Category, Cart, CartProduct, FavoriteList, Rating, Review, Coupon, Brand
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartProductSerializer, FavoritelistSerializer, RatingSerializer, ReviewSerializer, CouponSerializer, BrandSerializer
from .filters import ProductFilter, BrandFilter
from utility.views import BaseAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

class CategoryList(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandList(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [AllowAny]  
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BrandFilter
    
class BrandDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny] 
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    
class ProductList(BaseAPIView, generics.ListCreateAPIView):
    
    def get(self, request, *args, **kwargs):
        print('8'*10)
        return super().get(request, *args, **kwargs)
    
    permission_classes = [AllowAny]
    queryset = Product.objects.annotate(average_rating=Avg('ratings__score'))
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class ProductDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartView(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartProductsDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.quantity = request.data.get("quantity", instance.quantity)
        instance.save()
        return Response(
            {"message": "به روز رسانی با موفقیت انجام شد "}, status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "محصول از سبد خرید حذف شد"}, status=status.HTTP_204_NO_CONTENT
        )


class FavoriteListView (BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FavoriteList.objects.all()
    serializer_class = FavoritelistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FavoriteList.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous: 
            raise PermissionDenied("برای دسترسی به این عمل، باید وارد سیستم شوید.")
        
        favorite_list, created = FavoriteList.objects.get_or_create(user=request.user)
        
        product_id = request.data.get("product_id")
        product = Product.objects.get(id=product_id)
        
        favorite_list.product.add(product)
        return Response({"message": "محصول به لیست علاقه مندی اضافه شد"}, status=status.HTTP_201_CREATED)
        
class RemoveFromFavoriteList(BaseAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FavoriteList.objects.all()
    serializer_class = FavoritelistSerializer
    
    def delete(self, request, *args, **kwargs):    
        FavoriteList = FavoriteList.objects.get(user=request.user)
        product_id = request.data.get("product_id")
        product = Product.objects.get(id=product_id)
        FavoriteList.product.remove(product)
        return Response({"message": "محصول از لیست علاقه مندی حذف شد"}, status=status.HTTP_204_NO_CONTENT)
    
class RatingView(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']
    
    
class ReviewView(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']
    
class CouponListCreateView(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

class CouponRetrieveUpdateDestroyView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    