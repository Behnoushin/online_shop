from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from utility.views import BaseAPIView

class OrderView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset.filter(user=user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        order.update_total_amount() 

class OrderDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        order = serializer.save()
        order.update_total_amount() 

class OrderItemView(BaseAPIView, generics.ListCreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return OrderItem.objects.filter(order_id=order_id)

    def perform_create(self, serializer):
        order_id = self.kwargs['order_id']
        order_item = serializer.save(order_id=order_id)
        order_item.order.update_total_amount()  
