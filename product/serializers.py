from .models import Product, Category, Cart, CartProduct, FavoriteList, Rating, Review , Coupon, Brand
from utility.serializers import BaseSerializer
from user_management.models import CustomUser
from rest_framework import serializers

class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BrandSerializer(BaseSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

class ProductSerializer(BaseSerializer):
    category = CategorySerializer()
    average_rating = serializers.FloatField(read_only=True)

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
        fields = '__all__'
        read_only_fields = ['used_count', 'created_at']
        
    def validate_discount_value(self, value):
        if value > 100:
            raise serializers.ValidationError("Discount value cannot exceed 100%.")
        return value
    
    def validate(self, data):
        if data['valid_from'] > data['valid_until']:
            raise serializers.ValidationError("The 'valid_from' date cannot be later than 'valid_until'.")
        return data