from .models import Product, Category, Cart, CartProduct, FavoriteList, Rating, Review, Coupon
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartProductSerializer, FavoritelistSerializer, RatingSerializer, ReviewSerializer, CouponSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from utility.views import BaseAPIView


class ProductList(BaseAPIView, generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all()
        title = self.request.query_params.get('title', None)
        category = self.request.query_params.get('category', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if title:
            queryset = queryset.filter(title__icontains=title)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

class ProductDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryList(BaseAPIView, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartProductsDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
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
    queryset = FavoriteList.objects.all()
    serializer_class = FavoritelistSerializer
    
    def delete(self, request, *args, **kwargs):    
        FavoriteList = FavoriteList.objects.get(user=request.user)
        product_id = request.data.get("product_id")
        product = Product.objects.get(id=product_id)
        FavoriteList.product.remove(product)
        return Response({"message": "محصول از لیست علاقه مندی حذف شد"}, status=status.HTTP_204_NO_CONTENT)
    
class RatingView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
class ReviewView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
class CouponListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

class CouponRetrieveUpdateDestroyView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    

