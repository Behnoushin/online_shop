from .models import AboutUs, ContactUs, FAQ
from .serializers import AboutUsSerializer, ContactUsSerializer, FAQSerializer
from rest_framework import generics
from utility.views import BaseAPIView

class AboutUsList(BaseAPIView, generics.ListCreateAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

    def get_queryset(self):
        return super().get_queryset()

class AboutUsDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer


class ContactUsList(BaseAPIView, generics.ListCreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer


class ContactUsDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer


class FAQList(BaseAPIView, generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class FAQDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer