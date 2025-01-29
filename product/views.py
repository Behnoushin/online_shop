from .models import Product, Category, Cart, CartProduct, FavoriteList, Rating, Review, Coupon, Brand
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartProductSerializer, FavoritelistSerializer, RatingSerializer, ReviewSerializer, CouponSerializer, BrandSerializer
from .filters import ProductFilter, BrandFilter
from utility.views import BaseAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Sum, Count

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
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category', None)
        brand_id = self.request.query_params.get('brand', None)
        
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if brand_id:
            queryset = queryset.filter(brand__id=brand_id)
            
        return queryset


class ProductDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        ratings = Rating.objects.filter(product=product)
        reviews = Review.objects.filter(product=product)
        average_rating = ratings.aggregate(Avg('score'))['score__avg']
        response_data = {
            'product': ProductSerializer(product).data,
            'average_rating': average_rating,
            'reviews': ReviewSerializer(reviews, many=True).data
        }
        return Response(response_data)


class TopSellingProducts(BaseAPIView, generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        top_selling_products = Product.objects.annotate(total_sales=Sum('orderitem__quantity'))
        return top_selling_products.filter(total_sales__gt=0).order_by('-total_sales')[:10]


class PopularProductsView(BaseAPIView, generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.annotate(
            total_reviews=Count('review', distinct=True),
            avg_rating=Avg('rating__score')
        ).order_by('-total_reviews', '-avg_rating')[:10]


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
    
    def get_queryset(self):
        return FavoriteList.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous: 
            raise PermissionDenied("برای دسترسی به این عمل، باید وارد سیستم شوید.")
        
        favorite_list, created = FavoriteList.objects.get_or_create(user=request.user)
        
        product_id = request.data.get("product_id")
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "محصول پیدا نشد."}, status=status.HTTP_400_BAD_REQUEST)
        if favorite_list.has_product(product):
            message = f"محصول '{product.name}' قبلاً در لیست علاقه‌مندی‌ها وجود داشته است."
        else:        
            favorite_list.add_product(product)
            message = f"لیست علاقه‌مندی‌ها به‌روزرسانی شد و محصول '{product.name}' اضافه شد."
            
        return Response(
            {
                "message": message,
                "product_id": product_id,
                "favorite_list_id": favorite_list.id
            },
            status=status.HTTP_200_OK
        )        
        
        
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
    
    def perform_create(self, serializer):
        if Rating.objects.filter(user=self.request.user, product=serializer.validated_data['product']).exists():
            raise ValidationError("شما قبلاً امتیاز داده‌اید.")
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "امتیاز شما ثبت شد", "data": response.data}, status=status.HTTP_201_CREATED)   
    
    
class ReviewView(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "نظر شما ثبت شد", "data": response.data}, status=status.HTTP_201_CREATED)    
    
    
class CouponListCreateView(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        active = self.request.query_params.get('active')
        if active is not None:
            queryset = queryset.filter(active=active)
        return queryset


class CouponRetrieveUpdateDestroyView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    
    def perform_update(self, serializer):
        instance = serializer.save()


class ValidateCouponView(BaseAPIView, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CouponSerializer

    def post(self, request, *args, **kwargs):
        code = request.data.get("code")
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            return Response({"valid": True, "discount": coupon.discount}, status=status.HTTP_200_OK)
        except Coupon.DoesNotExist:
            return Response({"valid": False, "message": "کد تخفیف نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)
