from rest_framework import serializers
from .models import UserProfile, PurchaseHistory
from product.serializers import ProductSerializer
from .models import CustomUser
from utility.serializers import BaseSerializer

class UserProfileSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = UserProfile
        fields = "__all__"


class UserSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = CustomUser
        fields = "__all__"


class PurchaseHistorySerializer(BaseSerializer):
    product = ProductSerializer()

    class Meta(BaseSerializer.Meta):
        model = PurchaseHistory
        fields = "__all__"
    
class OTPSerializer(BaseSerializer):
    email = serializers.EmailField()
    otp_code = serializers.IntegerField()

    class Meta(BaseSerializer.Meta):
        model = CustomUser
        fields = ['email', 'otp_code']