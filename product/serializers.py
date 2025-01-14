from .models import Product, Category, Cart, CartProduct, FavoriteList, Rating, Review , Coupon
from utility.serializers import BaseSerializer
from rest_framework import serializers

class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
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
    class Meta:
        model = Review
        fields = "__all__"
        
class CouponSerializer(BaseSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'