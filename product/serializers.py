from rest_framework import serializers
from .models import (
    Product, Category, Cart, CartProduct, FavoriteList, Rating, 
    Review, Coupon, Warranty, Brand, Question, Answer, Comment,
    Report, RatingBrand, ReviewBrand,
)
from user_management.models import CustomUser
from utility.serializers import BaseSerializer


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BrandSerializer(BaseSerializer):
    class Meta:
        model = Brand
        fields = "__all__"
        
        
        
class WarrantySerializer(BaseSerializer):
    class Meta:
        model = Warranty
        fields = "__all__"


class ProductSerializer(BaseSerializer):
    category = CategorySerializer()
    average_rating = serializers.FloatField(read_only=True)
    total_sales = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Product
        fields = "__all__"


class CartProductSerializer(BaseSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = CartProduct
        fields = "__all__"


class CartSerializer(BaseSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class FavoritelistSerializer(BaseSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = FavoriteList
        fields = "__all__"
        
class RatingBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingBrand
        fields = "__all__"
        read_only_fields = ['user', 'status']


class ReviewBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewBrand
        fields = "__all__"
        read_only_fields = ['user', 'like', 'dislike']



class RatingSerializer(BaseSerializer):
    class Meta:
        model = Rating
        fields = "__all__"
 
        
class ReviewSerializer(BaseSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all()) 
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 
    like = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True) 
    dislike = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    parent_review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(), required=False)
    
    class Meta:
        model = Review
        fields = "__all__"
        
        
class CouponSerializer(BaseSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"
        read_only_fields = ['used_count', 'created_at']
        
    def validate_discount_value(self, value):
        """
        Ensure discount value does not exceed 100%.
        """
        if value > 100:
            raise serializers.ValidationError("Discount value cannot exceed 100%.")
        return value
    
    def validate(self, data):
        """
        Ensure 'valid_from' date is earlier than 'valid_until' date.
        """
        if data['valid_from'] > data['valid_until']:
            raise serializers.ValidationError("The 'valid_from' date cannot be later than 'valid_until'.")
        return data

    
class AnswerSerializer(BaseSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
           
            
class QuestionSerializer(BaseSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    upvotes = serializers.IntegerField(read_only=True)
    downvotes = serializers.IntegerField(read_only=True)
    best_answer = AnswerSerializer(read_only=True)

    class Meta:
        model = Question
        fields = "__all__"


class CommentSerializer(BaseSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = "__all__"
        

class ReportSerializer(BaseSerializer):
    class Meta:
        model = Report
        fields = "__all__"
