from rest_framework import serializers
from .models import UserProfile, PurchaseHistory, Address
from product.serializers import ProductSerializer
from .models import CustomUser
from utility.serializers import BaseSerializer

class AddressSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Address
        fields = "__all__"

class UserProfileSerializer(BaseSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta(BaseSerializer.Meta):
        model = UserProfile
        fields = "__all__"


class UserSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = CustomUser
        fields = "__all__"

class UserProfileUpdateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = "__all__"
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


class PurchaseHistorySerializer(BaseSerializer):
    product = ProductSerializer()
    address = AddressSerializer()
    total_cost = serializers.SerializerMethodField()

    class Meta(BaseSerializer.Meta):
        model = PurchaseHistory
        fields = "__all__"
        
    def get_total_cost(self, obj):
        return obj.total_cost()
    
class EmailSerializer(BaseSerializer):
    email = serializers.EmailField()
    class Meta:
        model = CustomUser
        fields = ['email']
