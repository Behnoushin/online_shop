from rest_framework import serializers
from .models import UserProfile, PurchaseHistory
from product.serializers import ProductSerializer
from .models import CustomUser


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "phone_number", "age"]


class PurchaseHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = PurchaseHistory
        fields = "__all__"