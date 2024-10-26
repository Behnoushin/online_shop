from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ProductSerializer
from utility.serializers import BaseSerializer

class OrderItemSerializer(BaseSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(BaseSerializer):
    products = ProductSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = Order
        fields = "__all__"
