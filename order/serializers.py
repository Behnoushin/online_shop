# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import Order, OrderItem, Payment
from product.serializers import ProductSerializer
from utility.serializers import BaseSerializer
from product.models import Product

##################################################################################
#                      OrderItemSerializer serializers                           #
##################################################################################

class OrderItemSerializer(BaseSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = "__all__"

    def validate_quantity(self, value):
        try:
            product_id = self.initial_data.get('product')
            product = Product.objects.get(id=product_id)
            stock = product.stock
        
            if value > stock:
                raise serializers.ValidationError("Quantity exceeds available stock.")
        
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product.")
        
        return value

        
##################################################################################
#                          OrderSerializer serializers                           #
##################################################################################

class OrderSerializer(BaseSerializer):
    items = OrderItemSerializer(many=True)  
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta(BaseSerializer.Meta):
        model = Order
        fields = "__all__"
        

##################################################################################
#                      PaymentSerializer serializers                             #
##################################################################################

class PaymentSerializer(BaseSerializer):
    payment_method = serializers.CharField(max_length=50)  
    final_amount = serializers.DecimalField(max_digits=10, decimal_places=2) 

    class Meta:
        model = Payment
        fields = "__all__"
    
    def validate(self, data):
        order = data.get('order') or getattr(self.instance, 'order', None)
        payment_status = data.get('payment_status', getattr(self.instance, 'payment_status', None))
        
        if order.status == Order.CANCELED and payment_status == 'paid':
            raise serializers.ValidationError("Cannot mark payment as paid for a canceled order.")
        
        return data

