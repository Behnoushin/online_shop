from django.urls import path
from .views import ShippingMethodView, ShipmentView

urlpatterns = [
    path("shipping-methods/", ShippingMethodView.as_view(), name="shipping-methods"),
    path("shipments/", ShipmentView.as_view(), name="shipments"),
    path("shipment/<int:pk>/", ShipmentView.as_view(), name="shipment-detail"),
    path("shipment/<int:pk>/update-status/", ShipmentView.as_view(), name="shipment-status-update"),
    path("shipment/<int:pk>/estimated-delivery/", ShipmentView.as_view(), name="estimated-delivery-time"),
]
