from rest_framework import serializers
from .models import Order, OrderItem, Payment
from product.serializers import ProductSerializer
from utility.serializers import BaseSerializer

class OrderItemSerializer(BaseSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(BaseSerializer):
    items = OrderItemSerializer(many=True)  
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta(BaseSerializer.Meta):
        model = Order
        fields = "__all__"


class PaymentSerializer(BaseSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    payment_method = serializers.CharField(max_length=50)  
    payment_status = serializers.ChoiceField(choices=[('pending', 'Pending'), ('paid', 'Paid')]) 
    transaction_id = serializers.CharField(max_length=100, required=False, allow_blank=True)  
    payment_date = serializers.DateTimeField(read_only=True) 
    final_amount = serializers.DecimalField(max_digits=10, decimal_places=2) 

    class Meta:
        model = Payment
        fields = "__all__"
