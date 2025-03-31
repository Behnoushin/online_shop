from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer
from .permissions import IsOwnerOrAdmin
from utility.views import BaseAPIView


# -----------------------------------------------------------------------------
#  Order Views
# -----------------------------------------------------------------------------

class OrderView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter orders by status and user, handle invalid status errors.
        """
        user = self.request.user
        status = self.request.query_params.get('status', None)

        if status and status not in [s[0] for s in Order.STATUS_CHOICES]:
            return Response({
                "error": "Invalid status value provided."
            }, status=status.HTTP_400_BAD_REQUEST)

        queryset = Order.objects.filter(user=user)
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset

    def perform_create(self, serializer):
        """
        Create an order and update the total amount.
        """
        order = serializer.save(user=self.request.user)
        order.update_total_amount()


class OrderDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Update the order and recalculate the total amount.
        """
        order = serializer.save()
        order.update_total_amount()

    def perform_destroy(self, instance):
        """
        Handle any custom logic before deleting the order, if needed.
        """
        super().perform_destroy(instance)

# -----------------------------------------------------------------------------
#  OrderItem Views
# -----------------------------------------------------------------------------

class OrderItemView(BaseAPIView, generics.ListCreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter order items by the order ID.
        """
        order_id = self.kwargs['order_id']
        return OrderItem.objects.filter(order_id=order_id)

    def perform_create(self, serializer):
        """
        Create an order item and update the total amount of the related order.
        """
        order_id = self.kwargs['order_id']
        order_item = serializer.save(order_id=order_id)
        order_item.order.update_total_amount()
        
    def perform_update(self, serializer):
        """
        Handle updating order items and recalculating the total amount.
        """
        order_item = serializer.save()
        order_item.order.update_total_amount()

    def create(self, request, *args, **kwargs):
        """
        Custom response for successful order item creation.
        """
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Order item successfully created",
            "order_item": response.data
        }, status=status.HTTP_201_CREATED)
        
# -----------------------------------------------------------------------------
#  Payment Views
# -----------------------------------------------------------------------------

class PaymentListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsOwnerOrAdmin]  

    def perform_create(self, serializer):
        """
        Saves the current logged-in user as the 'user' field in the Order when creating the payment
        """
        serializer.save(order__user=self.request.user)


class PaymentDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsOwnerOrAdmin] 