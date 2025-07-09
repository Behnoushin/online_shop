# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import UserProfile, PurchaseHistory, Address, CustomUser
from product.serializers import ProductSerializer
from utility.serializers import BaseSerializer

##################################################################################
#                      AddressSerializer serializers                             #
##################################################################################

class AddressSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Address
        fields = "__all__"
        
    def validate_postal_code(self, value):
        """
        Validates that the postal code consists only of digits
        and is exactly 10 characters long.
        """
        if value:
            if not value.isdigit():
                raise serializers.ValidationError("Postal code must contain only digits.")
            if len(value) != 10:
                raise serializers.ValidationError("Postal code must be exactly 10 digits long.")
        return value
                
##################################################################################
#                      UserProfileSerializer serializers                         #
##################################################################################

class UserProfileSerializer(BaseSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta(BaseSerializer.Meta):
        model = UserProfile
        fields = "__all__"

##################################################################################
#                      UserSerializer serializers                                #
##################################################################################

class UserSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = CustomUser
        fields = "__all__"

    def validate_age(self, value):
        if value is None or value < 13:
            raise serializers.ValidationError("Age must be at least 13 years old.")
        return value

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if not (10 <= len(value) <= 15):
            raise serializers.ValidationError("Phone number length must be between 10 and 15 digits.")
        return value

##################################################################################
#                  UserProfileUpdateSerializer serializers                       #
##################################################################################

class UserProfileUpdateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = "__all__"
        
##################################################################################
#                    ChangePasswordSerializer serializers                        #
##################################################################################

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

##################################################################################
#                  PurchaseHistorySerializer serializers                         #
##################################################################################


class PurchaseHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for PurchaseHistory model.
    Handles product name, quantity, price, and formatted purchase date.
    Validates quantity to be at least 1.
    purchase_date is read-only and formatted as 'YYYY-MM-DD HH:mm:ss'.
    """
    purchase_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = PurchaseHistory
        fields = ['id', 'product_name', 'quantity', 'price', 'purchase_date']
        read_only_fields = ['id', 'purchase_date']

##################################################################################
#                        EmailSerializer serializers                             #
##################################################################################

class EmailSerializer(BaseSerializer):
    email = serializers.EmailField()
    class Meta:
        model = CustomUser
        fields = ['email']
