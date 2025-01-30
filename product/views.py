from .models import Product, Category, Cart, CartProduct, FavoriteList, Rating, Review, Coupon, Brand, Question, Answer
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartProductSerializer, FavoritelistSerializer, RatingSerializer, ReviewSerializer, CouponSerializer, BrandSerializer, QuestionSerializer, AnswerSerializer
from .filters import ProductFilter, BrandFilter
from utility.views import BaseAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Sum, Count
from django.shortcuts import get_object_or_404


class CategoryList(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        categories = self.get_queryset()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser] 
        return super().post(request, *args, **kwargs)
    
    
class CategoryDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser] 
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]  
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]  
        return super().delete(request, *args, **kwargs)


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
        return Response({"message": "به روز رسانی با موفقیت انجام شد "}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "محصول از سبد خرید حذف شد"}, status=status.HTTP_204_NO_CONTENT)


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
            message = f"محصول '{product.title}' قبلاً در لیست علاقه‌مندی‌ها وجود داشته است."
        else:        
            favorite_list.add_product(product)
            message = f"لیست علاقه‌مندی‌ها به‌روزرسانی شد و محصول '{product.title}' اضافه شد."
            
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


class ReviewEditDelete(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_object(self):
        return get_object_or_404(Review, user=self.request.user, product=self.kwargs['product_id'])
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "نظر شما به روز رسانی شد."}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return Response({"message": "نظر شما حذف شد."}, status=status.HTTP_204_NO_CONTENT)

    
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


class QuestionList(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        question = serializer.save(user=self.request.user)
        return Response({"message": "سوال شما با موفقیت ثبت شد."}, status=status.HTTP_201_CREATED)       
     
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
    
        for question_data in serializer.data:
            question = Question.objects.get(id=question_data['id'])
            question_data['upvotes'] = question.upvotes
            question_data['downvotes'] = question.downvotes
            question_data['is_best'] = question.is_best
            
            if question.best_answer:
                question_data['best_answer'] = AnswerSerializer(question.best_answer).data           
            
        return Response(serializer.data)       
    

class QuestionDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_update(self, serializer):
        question = serializer.instance
        
        if not self.request.user.is_staff and self.request.user != serializer.instance.user:
            raise PermissionDenied("شما نمی توانید سوال شخص دیگری را ویرایش کنید.")

        if 'mark_best' in self.request.data:
            if not self.request.user.is_staff:
                raise PermissionDenied("فقط مدیران می‌توانند بهترین سوال را مشخص کنند.")
            
            Question.objects.all().update(is_best=False)
            question.is_best = True
            question.save()
            return Response({"message": "سوال به عنوان بهترین انتخاب شد."}, status=status.HTTP_200_OK)


        if 'upvote' in self.request.data:
            serializer.instance.upvotes += 1
            serializer.instance.save()
            return Response({"message": "رای مثبت شما ثبت شد."}, status=status.HTTP_200_OK)
        
        elif 'downvote' in self.request.data:
            serializer.instance.downvotes += 1
            serializer.instance.save()
            return Response({"message": "رای منفی شما ثبت شد."}, status=status.HTTP_200_OK)
        
        return super().perform_update(serializer)


class AnswerList(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    
    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return Answer.objects.filter(question_id=question_id)
    
    def perform_create(self, serializer):
        question = Question.objects.get(id=self.kwargs['question_id']) 
        answer = serializer.save(user=self.request.user, question=question)
        return Response({"message": "پاسخ شما با موفقیت ثبت شد."}, status=status.HTTP_201_CREATED)

class AnswerDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_update(self, serializer):
        answer = serializer.instance
        question = answer.question
        
        if not self.request.user.is_staff and self.request.user != serializer.instance.user:
            raise PermissionDenied("شما نمی توانید پاسخ شخص دیگری را ویرایش کنید.")
        
        if 'mark_best' in self.request.data:
            question = answer.question
            if question.user != self.request.user:
                raise PermissionDenied("فقط نویسنده سوال می‌تواند پاسخ برتر را انتخاب کند.")
            
            question.best_answer = answer
            question.save()
            return Response({"message": "پاسخ به عنوان بهترین انتخاب شد"}, status=status.HTTP_200_OK)
        
        if 'upvote' in self.request.data:
            serializer.instance.upvotes += 1
            serializer.instance.save()
            return Response({"message": "رای مثبت شما ثبت شد."}, status=status.HTTP_200_OK)
        
        elif 'downvote' in self.request.data:
            serializer.instance.downvotes += 1
            serializer.instance.save()
            return Response({"message": "رای منفی شما ثبت شد."}, status=status.HTTP_200_OK)
        
        return super().perform_update(serializer)


class SimilarProductsView(BaseAPIView, generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')

        if product_id is None:
            raise ValidationError({'error': 'شناسه محصول مورد نیاز است.'})

        try:
            product_id = int(product_id)
        except ValueError:
            raise ValidationError({'error': 'شناسه محصول نامعتبر است.'})

        product = get_object_or_404(Product, id=product_id)

        similar_products = (
            Product.objects
            .filter(category=product.category, brand=product.brand)
            .exclude(id=product.id)
            .annotate(avg_rating=Avg('rating__score'))
            .order_by('-avg_rating')[:5]
        )        
        
        return similar_products
