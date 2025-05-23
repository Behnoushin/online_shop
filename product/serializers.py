# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import (
    Product, Category, Cart, CartProduct, FavoriteList, Rating, 
    Review, Coupon, Warranty, Brand, Question, Answer, Comment,
    Report, RatingBrand, ReviewBrand,
)
from user_management.models import CustomUser
from utility.serializers import BaseSerializer

##################################################################################
#                      CategorySerializer serializers                            #
##################################################################################

class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = "__all__"

##################################################################################
#                      BrandSerializer serializers                               #
##################################################################################

class BrandSerializer(BaseSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

##################################################################################
#                      WarrantySerializer serializers                            #
##################################################################################

class WarrantySerializer(BaseSerializer):
    class Meta:
        model = Warranty
        fields = "__all__"

    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data

##################################################################################
#                       ProductSerializer serializers                            #
##################################################################################

class ProductSerializer(BaseSerializer):
    category = CategorySerializer()
    average_rating = serializers.FloatField(read_only=True)
    total_sales = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value

##################################################################################
#                    CartProductSerializer serializers                           #
##################################################################################

class CartProductSerializer(BaseSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = "__all__"

##################################################################################
#                          CartSerializer serializers                            #
##################################################################################

class CartSerializer(BaseSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

##################################################################################
#                     FavoritelistSerializer serializers                         #
##################################################################################

class FavoritelistSerializer(BaseSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = FavoriteList
        fields = "__all__"

##################################################################################
#               Rating and Review Brand Serializer serializers                   #
##################################################################################

class RatingBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingBrand
        fields = "__all__"
        read_only_fields = ['user', 'status']

    def validate_score(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError("The score should be between 0 and 5.")
        return value

class ReviewBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewBrand
        fields = "__all__"
        read_only_fields = ['user', 'like', 'dislike']

##################################################################################
#               Rating and Review Product Serializer serializers                 #
##################################################################################

class RatingSerializer(BaseSerializer):
    class Meta:
        model = Rating
        fields = "__all__"

    def validate_score(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError("The score should be between 0 and 5.")
        return value


class ReviewSerializer(BaseSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all()) 
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 
    like = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True) 
    dislike = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    parent_review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(), required=False)

    class Meta:
        model = Review
        fields = "__all__"

##################################################################################
#                          CouponSerializer serializers                          #
##################################################################################

class CouponSerializer(BaseSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"
        read_only_fields = ['used_count', 'created_at']

    def validate_discount_value(self, value):
        """
        Discount amount must be between 0 and 100.
        """
        if not (0 <= value <= 100):
            raise serializers.ValidationError("Discount amount must be between 0 and 100.")
        return value

    def validate(self, data):
        """
        Ensure 'valid_from' date is earlier than 'valid_until' date.
        """
        if data['valid_from'] > data['valid_until']:
            raise serializers.ValidationError("The 'valid_from' date cannot be later than 'valid_until'.")
        return data

##################################################################################
#                  Question and Answer Serializer serializers                    #
##################################################################################

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

##################################################################################
#                          CommentSerializer serializers                         #
##################################################################################

class CommentSerializer(BaseSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = "__all__"

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment text cannot be empty.")
        return value

##################################################################################
#                          ReportSerializer serializers                          #
##################################################################################

class ReportSerializer(BaseSerializer):
    class Meta:
        model = Report
        fields = "__all__"
