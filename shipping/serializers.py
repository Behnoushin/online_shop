# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import ShippingMethod, Shipment
from utility.serializers import BaseSerializer

##################################################################################
#                      ShippingMethodSerialize serializers                       #
##################################################################################

class ShippingMethodSerializer(BaseSerializer):
    class Meta:
        model = ShippingMethod
        fields = '__all__'

    def get_shipping_cost(self, obj):
        weight = self.context.get('weight', self.initial_data.get('weight', 10))  
        distance = self.context.get('distance', self.initial_data.get('distance', 100))
        return obj.calculate_shipping_cost(weight, distance)

##################################################################################
#                         ShipmentSerializer serializers                         #
##################################################################################

class ShipmentSerializer(BaseSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'
