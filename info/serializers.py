from rest_framework import serializers
from .models import AboutUs, ContactUs, FAQ
from utility.serializers import BaseSerializer

class AboutUsSerializer(BaseSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"


class ContactUsSerializer(BaseSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"


class FAQSerializer(BaseSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"