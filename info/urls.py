from django.urls import path
from .views import (
    AboutUsList, AboutUsDetail, 
    ContactUsList, ContactUsDetail,
    FAQList, FAQDetail,
    LocationMapListCreateView, LocationMapDetailView,
    TeamMemberListCreateView, TeamMemberDetailView,
    SiteStatListCreateView, SiteStatDetailView,
    TermsAndConditionsListCreateView, TermsAndConditionsDetailView,
    PrivacyPolicyListCreateView, PrivacyPolicyDetailView
)

urlpatterns = [
    
    # AboutUs URLs
    path("about/", AboutUsList.aas_view(), name="about-list"),
    path("about/<int:pk>/", AboutUsDetail.as_view(), name="about-detail"),
    
    # Contact Us URLs
    path("contact/", ContactUsList.as_view(), name="contact-list"),
    path("contact/<int:pk>/", ContactUsDetail.as_view(), name="contact-detail"),
    
    # FAQ URLs
    path("faq/", FAQList.as_view(), name="faq-list"),
    path("faq/<int:pk>/", FAQDetail.as_view(), name="faq-detail"),
    
    # LocationMap URLs
    path("location-map/", LocationMapListCreateView.as_view(), name="location-map-list"),
    path("location-map/<int:pk>/", LocationMapDetailView.as_view(), name="location-map-detail"),
    
    # TeamMember URLs
    path("team-member/", TeamMemberListCreateView.as_view(), name="team-member-list"),
    path("team-member/<int:pk>/", TeamMemberDetailView.as_view(), name="team-member-detail"),
    
    # SiteStat URLs
    path("site-stat/", SiteStatListCreateView.as_view(), name="site-stat-list"),
    path("site-stat/<int:pk>/", SiteStatDetailView.as_view(), name="site-stat-detail"),
    
    # Terms And Conditions URLs
    path("terms-and-conditions/", TermsAndConditionsListCreateView.as_view(), name="terms-and-conditions-list"),
    path("terms-and-conditions/<int:pk>/", TermsAndConditionsDetailView.as_view(), name="terms-and-conditions-detail"),
    
    # Privacy Policy URLs
    path("privacy-policy/", PrivacyPolicyListCreateView.as_view(), name="privacy-policy-list"),
    path("privacy-policy/<int:pk>/", PrivacyPolicyDetailView.as_view(), name="privacy-policy-detail"),
    
]
