from rest_framework import serializers
from .models import Product, Category, Cart, CartProduct, FavoriteList, Rating, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = CartProduct
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

class FavoritelistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = FavoriteList
        fields = "__all__"

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model:Rating
        fields = "__all__"
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model:Review
        fields = "__all__"