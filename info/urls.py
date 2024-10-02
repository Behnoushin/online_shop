from django.urls import path
from .views import AboutUsList, AboutUsDetail, ContactUsList, ContactUsDetail, FAQList, FAQDetail

urlpatterns = [
    path("about/", AboutUsList.as_view(), name="about-list"),
    path("about/<int:pk>/", AboutUsDetail.as_view(), name="about-detail"),
    path("contact/", ContactUsList.as_view(), name="contact-list"),
    path("contact/<int:pk>/", ContactUsDetail.as_view(), name="contact-detail"),
    path("faq/", FAQList.as_view(), name="faq-list"),
    path("faq/<int:pk>/", FAQDetail.as_view(), name="faq-detail"),
]