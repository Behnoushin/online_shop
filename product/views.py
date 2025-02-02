from .models import (
    Product, Category, Cart, CartProduct, FavoriteList, Rating, 
    Review, Coupon, Warranty, Brand, Question, Answer, Comment,
    Report,
)
from .serializers import (
    ProductSerializer, CategorySerializer, CartSerializer, 
    CartProductSerializer, FavoritelistSerializer, RatingSerializer, 
    ReviewSerializer, CouponSerializer, WarrantySerializer, 
    BrandSerializer, QuestionSerializer, AnswerSerializer,
    CommentSerializer, ReportSerializer,
)
from .filters import ProductFilter, BrandFilter
from utility.views import BaseAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Sum, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone

# -----------------------------------------------------------------------------
# Category Views
# -----------------------------------------------------------------------------

class CategoryList(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        """
        Get all categories.
        """
        categories = self.get_queryset()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a new category (only accessible by admin).
        """
        self.permission_classes = [IsAdminUser] 
        return super().post(request, *args, **kwargs)
    
    
class CategoryDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        """
        Get a specific category by ID.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Update an existing category (only accessible by admin).
        """
        self.permission_classes = [IsAdminUser] 
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Partially update an existing category (only accessible by admin).
        """
        self.permission_classes = [IsAdminUser]  
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete an existing category (only accessible by admin).
        """
        self.permission_classes = [IsAdminUser]  
        return super().delete(request, *args, **kwargs)

# -----------------------------------------------------------------------------
# Brand Views
# -----------------------------------------------------------------------------

class BrandList(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [AllowAny]  
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BrandFilter
    
    def post(self, request, *args, **kwargs):
        """
        Create a new brand. Only admins can do this.
        """
        if not request.user.is_staff:
            return Response({'detail': 'شما اجازه ایجاد برند را ندارید.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BrandDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]  
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_permissions(self):
        """
        Define permissions based on the request method.
        Admins can update or delete, everyone else can view.
        """
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminUser()] 
        return [AllowAny()] 
    

    def get_object(self):
        """
        Get the brand or return error if not found.
        """
        try:
            return super().get_object()
        except Brand.DoesNotExist:
            raise NotFound(detail="برند مورد نظر یافت نشد.")
        

    def put(self, request, *args, **kwargs):
        """
        Update the brand. Only admins can update.
        """
        try:
            response = super().put(request, *args, **kwargs)
            response.data['message'] = 'برند با موفقیت بروزرسانی شد.'
            return response
        except PermissionDenied:
            return Response({'detail': 'شما اجازه دسترسی به این عمل را ندارید.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'detail': f"خطا در بروزرسانی برند: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, *args, **kwargs):
        """
        Delete the brand. Only admins can delete.
        """
        try:
            response = super().delete(request, *args, **kwargs)
            return Response({'message': 'برند با موفقیت حذف شد.'}, status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied:
            return Response({'detail': 'شما اجازه دسترسی به این عمل را ندارید.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'detail': f"خطا در حذف برند: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
# -----------------------------------------------------------------------------
# Warranty Views
# -----------------------------------------------------------------------------

class WarrantyList(BaseAPIView, generics.ListCreateAPIView):
    queryset = Warranty.objects.all()
    serializer_class = WarrantySerializer

    def perform_create(self, serializer):
        """
        Save the new warranty object to the database.
        """
        serializer.save()


class WarrantyDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Warranty.objects.all()
    serializer_class = WarrantySerializer

    def get_warranty_status(self, warranty):
        """
        Return the warranty status based on the end date.
        """
        if warranty.end_date < timezone.now().date():
            return "منقضی شده"
        else:
            return "فعال"


    def get(self, request, *args, **kwargs):
        """
        Get warranty details for a product by its ID.
        """
        product_id = kwargs.get('product_id')
        try:
            warranty = Warranty.objects.get(product_id=product_id)
        except Warranty.DoesNotExist:
            return Response({"message": "این محصول گارانتی ندارد."}, status=status.HTTP_404_NOT_FOUND)
        
        status = self.get_warranty_status(warranty)
        data = {
            'product': warranty.product.name,
            'guarantee_duration': f"{warranty.start_date} تا {warranty.end_date}",
            'status': status,
            'remaining_time': str(warranty.end_date - timezone.now().date()) if status == 'فعال' else '0',
        }
        return Response(data, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        """
        Update warranty details for a product by its ID.
        """
        product_id = kwargs.get('product_id')
        try:
            warranty = Warranty.objects.get(product_id=product_id)
        except Warranty.DoesNotExist:
            return Response({"message": "این محصول گارانتی ندارد."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        warranty.start_date = data.get('start_date', warranty.start_date)
        warranty.end_date = data.get('end_date', warranty.end_date)
        warranty.save()
        return Response({"message": "گارانتی با موفقیت آپدیت شد."}, status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        """
        Delete the warranty for a product by its ID.
        """
        product_id = kwargs.get('product_id')
        try:
            warranty = Warranty.objects.get(product_id=product_id)
        except Warranty.DoesNotExist:
            return Response({"message": "این محصول گارانتی ندارد."}, status=status.HTTP_404_NOT_FOUND)

        warranty.delete()
        return Response({"message": "گارانتی با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------------------
# Product Views
# -----------------------------------------------------------------------------
    
class ProductList(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        """
        Get a list of products, filtered by category and brand if provided.
        """
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
        """
        Get product details along with its ratings and reviews.
        """
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
        """
        Get the top 10 selling products based on total sales.
        """
        top_selling_products = Product.objects.annotate(total_sales=Sum('orderitem__quantity'))
        return top_selling_products.filter(total_sales__gt=0).order_by('-total_sales')[:10]


class PopularProductsView(BaseAPIView, generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Get the top 10 most popular products based on reviews and ratings.
        """
        return Product.objects.annotate(
            total_reviews=Count('review', distinct=True),
            avg_rating=Avg('rating__score')
        ).order_by('-total_reviews', '-avg_rating')[:10]


class SimilarProductsView(BaseAPIView, generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Get similar products based on category and brand.
        """
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

# -----------------------------------------------------------------------------
# Cart Views
# -----------------------------------------------------------------------------

class CartView(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartProductsDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def update(self, request, *args, **kwargs):
        """
        Update product quantity in the cart. Only authenticated users can do this.
        """
        instance = self.get_object()
        instance.quantity = request.data.get("quantity", instance.quantity)
        instance.save()
        return Response({"message": "به روز رسانی با موفقیت انجام شد "}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Remove product from the cart. Only authenticated users can do this.
        """
        instance = self.get_object()
        instance.delete()
        return Response({"message": "محصول از سبد خرید حذف شد"}, status=status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------------------
# Favorite List Views
# -----------------------------------------------------------------------------

class FavoriteListView (BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FavoriteList.objects.all()
    serializer_class = FavoritelistSerializer
    
    def get_queryset(self):
        """
        Return the favorite list for the logged-in user.
        """
        return FavoriteList.objects.filter(user=self.request.user)
    
    
    def create(self, request, *args, **kwargs):
        """
        Add a product to the user's favorite list. 
        Requires the user to be logged in.
        """
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
        """
        Remove a product from the user's favorite list.
        """   
        FavoriteList = FavoriteList.objects.get(user=request.user)
        product_id = request.data.get("product_id")
        product = Product.objects.get(id=product_id)
        FavoriteList.product.remove(product)
        return Response({"message": "محصول از لیست علاقه مندی حذف شد"}, status=status.HTTP_204_NO_CONTENT)
    
# -----------------------------------------------------------------------------
# Rating and Review Views
# -----------------------------------------------------------------------------
    
class RatingView(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']
    
    def perform_create(self, serializer):
        """
        Check if the user already rated the product.
        """
        if Rating.objects.filter(user=self.request.user, product=serializer.validated_data['product']).exists():
            raise ValidationError("شما قبلاً امتیاز داده‌اید.")
        serializer.save(user=self.request.user)


    def create(self, request, *args, **kwargs):
        """
        Save the rating and return a success message.
        """
        response = super().create(request, *args, **kwargs)
        return Response({"message": "امتیاز شما ثبت شد", "data": response.data}, status=status.HTTP_201_CREATED)   
    
    
class ReviewView(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']
    
    def perform_create(self, serializer):
        """
        Save the review with the user who submitted it.
        """
        serializer.save(user=self.request.user)


    def create(self, request, *args, **kwargs):
        """
        Save the review and return a success message.
        """
        response = super().create(request, *args, **kwargs)
        return Response({"message": "نظر شما ثبت شد", "data": response.data}, status=status.HTTP_201_CREATED)    


class ReviewEditDelete(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_object(self):
        """
        Get the review of the current user for the specified product.
        """
        return get_object_or_404(Review, user=self.request.user, product=self.kwargs['product_id'])
    
    
    def update(self, request, *args, **kwargs):
        """
        Update the user's review for the specified product.
        """
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "نظر شما به روز رسانی شد."}, status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        """
        Delete the user's review for the specified product.
        """
        self.object = self.get_object()
        self.object.delete()
        return Response({"message": "نظر شما حذف شد."}, status=status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------------------
# Coupon Views
# -----------------------------------------------------------------------------
    
class CouponListCreateView(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]  
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    
    def get_queryset(self):
        """
        Filter coupons by 'active' status if provided.
        """
        queryset = super().get_queryset()
        active = self.request.query_params.get('active')
        if active is not None:
            queryset = queryset.filter(active=active)
        return queryset


    def perform_create(self, serializer):
        """
        Save a new coupon and return success message with coupon data.
        """
        instance = serializer.save()
        return Response({"message": "کوپن جدید با موفقیت ایجاد شد.", "coupon": CouponSerializer(instance).data}, status=status.HTTP_201_CREATED)


class CouponRetrieveUpdateDestroyView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser] 
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    
    def perform_update(self, serializer):
        """
        Update coupon and return success message with updated coupon data.
        """
        instance = serializer.save()
        return Response({"message": "کوپن با موفقیت به‌روزرسانی شد.", "coupon": CouponSerializer(instance).data}, status=status.HTTP_200_OK)
    
    
    def perform_destroy(self, instance):
        """
        Delete coupon and return success message.
        """
        instance.delete()
        return Response({"message": "کوپن با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)


class ValidateCouponView(BaseAPIView, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CouponSerializer

    def post(self, request, *args, **kwargs):
        """
        Validate a coupon code and return discount or error message.
        """
        code = request.data.get("code")
        try:
            coupon = Coupon.objects.get(code=code)

            if not coupon.active:
                return Response({"valid": False, "message": "کد تخفیف غیر فعال است."}, status=status.HTTP_400_BAD_REQUEST)

            if coupon.used_by:
                return Response({"valid": False, "message": "کد تخفیف قبلاً استفاده شده است."}, status=status.HTTP_400_BAD_REQUEST)

            if not coupon.is_admin_only and request.user.is_authenticated:
                return Response({"valid": False, "message": "ثبت کد تخفیف صرفاً از طرف ادمین امکان‌پذیر است."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"valid": True, "discount": coupon.discount}, status=status.HTTP_200_OK)

        except Coupon.DoesNotExist:
            return Response({"valid": False, "message": "کد تخفیف نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------------------
# Question and Answer Views
# -----------------------------------------------------------------------------

class QuestionList(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        """
        Create a new question and link it to the current user.
        """
        question = serializer.save(user=self.request.user)
        return Response({"message": "سوال شما با موفقیت ثبت شد."}, status=status.HTTP_201_CREATED)       
     
     
    def list(self, request, *args, **kwargs):
        """
        List all questions with additional data (upvotes, downvotes, etc.).
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for question_data in serializer.data:
            question = Question.objects.get(id=question_data['id'])
            question_data['upvotes'] = question.upvotes
            question_data['downvotes'] = question.downvotes
            question_data['is_best'] = question.is_best
            question_data['is_approved'] = question.is_approved
            
            if question.best_answer:
                question_data['best_answer'] = AnswerSerializer(question.best_answer).data

        return Response(serializer.data)      
    

class QuestionDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_update(self, serializer):
        """
        Update a question. Only the owner or admin can update.
        """
        question = serializer.instance
        
        if not self.request.user.is_staff and self.request.user != serializer.instance.user:
            raise PermissionDenied("شما نمی توانید سوال شخص دیگری را ویرایش کنید.")


        if 'mark_best' in self.request.data:
            """
            Mark the question as the best. Only admins can do this.
            """
            if not self.request.user.is_staff:
                raise PermissionDenied("فقط مدیران می‌توانند بهترین سوال را مشخص کنند.")
            
            Question.objects.all().update(is_best=False)
            question.is_best = True
            question.save()
            return Response({"message": "سوال به عنوان بهترین انتخاب شد."}, status=status.HTTP_200_OK)


        if 'approve' in self.request.data:
            """
            Approve the question by setting its approval status to True.
            """
            question.is_approved = True
            question.save()
            return Response({"message": "سوال تایید شد."}, status=status.HTTP_200_OK)
        
        
        if 'reject' in self.request.data:
            """
            Reject the question by setting its approval status to False.
            """
            question.is_approved = False
            question.save()
            return Response({"message": "سوال رد شد."}, status=status.HTTP_200_OK)


        if 'upvote' in self.request.data:
            """
            Upvote the question.
            """
            question.upvotes += 1
            question.save()
            return Response({"message": "رای مثبت شما ثبت شد."}, status=status.HTTP_200_OK)      
        
        
        elif 'downvote' in self.request.data:
            """
            Downvote the question.
            """
            question.downvotes += 1
            question.save()
            return Response({"message": "رای منفی شما ثبت شد."}, status=status.HTTP_200_OK)
        
        return super().perform_update(serializer)


class AnswerList(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    
    def get_queryset(self):
        """
        Filter answers by the associated question.
        """
        question_id = self.kwargs['question_id']
        return Answer.objects.filter(question_id=question_id)
    
    
    def perform_create(self, serializer):
        """
        Create a new answer for a specific question.
        """
        question = Question.objects.get(id=self.kwargs['question_id']) 
        answer = serializer.save(user=self.request.user, question=question)
        return Response({"message": "پاسخ شما با موفقیت ثبت شد."}, status=status.HTTP_201_CREATED)


    def list(self, request, *args, **kwargs):
        """
        List all answers with additional data (upvotes, downvotes, etc.).
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for answer_data in serializer.data:
            answer = Answer.objects.get(id=answer_data['id'])
            answer_data['upvotes'] = answer.upvotes
            answer_data['downvotes'] = answer.downvotes
            answer_data['is_approved'] = answer.is_approved

        return Response(serializer.data)
    
    
class AnswerDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_update(self, serializer):
        """
        Update an answer. Only the owner or admin can update.
        """
        answer = serializer.instance
        question = answer.question
        
        if not self.request.user.is_staff and self.request.user != serializer.instance.user:
            raise PermissionDenied("شما نمی توانید پاسخ شخص دیگری را ویرایش کنید.") 
        
        if 'mark_best' in self.request.data:
            """
            Mark the answer as the best for the associated question.
            Only the question owner can do this.
            """
            question = answer.question
            
            if question.user != self.request.user:
                raise PermissionDenied("فقط نویسنده سوال می‌تواند پاسخ برتر را انتخاب کند.")
            
            question.best_answer = answer
            question.save()
            return Response({"message": "پاسخ به عنوان بهترین انتخاب شد"}, status=status.HTTP_200_OK)
        
        
        if 'approve' in self.request.data:
            """
            Approve the answer and set its approval status to True.
            """
            answer.is_approved = True
            answer.save()
            return Response({"message": "پاسخ تایید شد."}, status=status.HTTP_200_OK)


        if 'reject' in self.request.data:
            """
            Reject the answer and set its approval status to False.
            """
            answer.is_approved = False
            answer.save()
            return Response({"message": "پاسخ رد شد."}, status=status.HTTP_200_OK)
        
        
        if 'upvote' in self.request.data:
            """
            Upvote the answer.
            """
            answer.upvotes += 1
            answer.save()
            return Response({"message": "رای مثبت شما ثبت شد."}, status=status.HTTP_200_OK)
        
        
        elif 'downvote' in self.request.data:
            """
            Downvote the answer.
            """
            answer.downvotes += 1
            answer.save()
            return Response({"message": "رای منفی شما ثبت شد."}, status=status.HTTP_200_OK)
        
        return super().perform_update(serializer)
    
    
class CommentList(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Returns comments related to a specific answer.
        """
        answer_id = self.kwargs['answer_id']
        return Comment.objects.filter(answer_id=answer_id)


    def perform_create(self, serializer):
        """
        Creates a new comment for a specific answer.
        """
        answer = Answer.objects.get(id=self.kwargs['answer_id'])
        comment = serializer.save(user=self.request.user, answer=answer)
        return Response({"message": "کامنت شما ثبت شد."}, status=status.HTTP_201_CREATED)


    def perform_update(self, serializer):
        """
        Updates an existing comment.
        """
        comment = serializer.instance
        if comment.user != self.request.user:
            return Response({"message": "شما نمی‌توانید کامنت دیگران را تغییر دهید."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer.save()
        return Response({"message": "کامنت شما تغییر کرد."}, status=status.HTTP_200_OK)


    def perform_destroy(self, instance):
        """
        Deletes a comment.
        """
        if instance.user != self.request.user:
            return Response({"message": "شما نمی‌توانید کامنت دیگران را حذف کنید."}, status=status.HTTP_403_FORBIDDEN)
        
        instance.delete()
        return Response({"message": "کامنت شما حذف شد."}, status=status.HTTP_204_NO_CONTENT)


class ReportList(BaseAPIView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        """
        Create a report for a question or answer.
        Validates content type (question or answer) and object ID.
        """
        content_type = self.request.data.get('content_type')
        object_id = self.request.data.get('object_id')

        if content_type not in ['question', 'answer']:
            return Response({"message": "نوع محتوا نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

        if content_type == 'question':
            content_object = Question.objects.get(id=object_id)
            
        else:
            content_object = Answer.objects.get(id=object_id)

        report = serializer.save(reported_by=self.request.user)
        return Response({"message": "گزارش تخلف شما با موفقیت ثبت شد."}, status=status.HTTP_201_CREATED)
