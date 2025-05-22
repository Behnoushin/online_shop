# -------------------   Django imports ------------------------
from django.shortcuts import get_object_or_404
# -------------------  DRF imports   ------------------------
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# -------------------   Apps imports ------------------------
from .models import ShippingMethod, Shipment
from .serializers import ShippingMethodSerializer, ShipmentSerializer
from utility.views import BaseAPIView

# -----------------------------------------------------------------------------
#  ShippingMethod Views
# -----------------------------------------------------------------------------
class ShippingMethodView(BaseAPIView, generics.ListCreateAPIView):
    queryset = ShippingMethod.objects.all()
    serializer_class = ShippingMethodSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the new shipping method.
        """
        serializer.save()


    def get_queryset(self):
        """
        Filter shipping methods by cost range if provided.
        """
        queryset = super().get_queryset()
        min_cost = self.request.query_params.get('min_cost', None)
        max_cost = self.request.query_params.get('max_cost', None)
        
        if min_cost:
            queryset = queryset.filter(cost__gte=min_cost)
        if max_cost:
            queryset = queryset.filter(cost__lte=max_cost)
        
        return queryset

# -----------------------------------------------------------------------------
#  Shipment Views
# -----------------------------------------------------------------------------

class ShipmentView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return shipments related to the current user.
        """
        user = self.request.user
        return Shipment.objects.filter(order__user=user)


    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user to the shipment's order
        and mark the order as shipped.
        """
        shipment = serializer.save(order__user=self.request.user)
        shipment.order.mark_as_shipped()


    def update_shipment_status(self, pk, status):
        """
        Update the shipment's status.
        """
        shipment = get_object_or_404(Shipment, pk=pk)
        if status == 'delivered':
            shipment.mark_as_delivered() 
        else:
            shipment.order_status = status
            shipment.save()
        return Response({"status": "updated"}, status=status.HTTP_200_OK)
    
    
    def get_estimated_delivery_time(self, pk):
        """
        Calculate the remaining days for estimated delivery.
        """
        shipment = Shipment.objects.get(pk=pk)
        remaining_days = shipment.estimated_days_left()
        return Response({"remaining_days": remaining_days}, status=status.HTTP_200_OK)
