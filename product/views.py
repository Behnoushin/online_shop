from .models import Product, Category, Cart, CartProduct, FavoriteList, Rating, Review
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartProductSerializer, FavoritelistSerializer, RatingSerializer, ReviewSerializer
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
        instance.quantity = request.data.get("quantity", instance.quantity)
        instance.save()
        return Response(
            {"message": "به روز رسانی با موفقیت انحام شد "}, status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "محصول از سبد خرید حذف شد"}, status=status.HTTP_204_NO_CONTENT
        )


class FavoriteListView (generics.ListCreateAPIView):
    queryset = FavoriteList.objects.all()
    serializer_class = FavoritelistSerializer
    
    def get_queryset(self):
        return FavoriteList.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        FavoriteList, created = FavoriteList.objects.get_or_create(user=request.user)
        product_id = request.data.get("product_id")
        product = Product.objects.get(id=product_id)
        FavoriteList.product.add(product)
        return Response({"message": "محصول به لیست علاقه مندی اضافه شد"}, status=status.HTTP_201_CREATED)
        
class RemoveFromFavoriteList(generics.DestroyAPIView):
    queryset = FavoriteList.objects.all()
    serializer_class = FavoritelistSerializer
    
    def delete(self, request, *args, **kwargs):    
        FavoriteList = FavoriteList.objects.get(user=request.user)
        product_id = request.data.get("product_id")
        product = Product.objects.get(id=product_id)
        FavoriteList.product.remove(product)
        return Response({"message": "محصول از لیست علاقه مندی حذف شد"}, status=status.HTTP_204_NO_CONTENT)
    
class RatingView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
class ReviewView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    