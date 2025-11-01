from django.urls import path
from .views import (
    AboutUsList, AboutUsDetail, AboutUsHistoryView, AboutUsRestoreView,
    ContactUsList, ContactUsDetail, ContactUsHistoryView, ContactUsRestoreView,
    FAQList, FAQDetail, FAQHistoryView, FAQRestoreView,
    LocationMapListCreateView, LocationMapDetail, LocationMapHistoryView, LocationMapRestoreView,
    TeamMemberListCreateView, TeamMemberDetailView, TeamMemberHistoryView, TeamMemberRestoreView,
    SiteStatListCreateView, SiteStatDetailView, SiteStatHistoryView, SiteStatRestoreView,
    TermsAndConditionsListCreateView, TermsAndConditionsDetailView, TermsAndConditionsHistoryView, TermsAndConditionsRestoreView,
    PrivacyPolicyListCreateView, PrivacyPolicyDetailView, PrivacyPolicyHistoryView, PrivacyPolicyRestoreView
)

urlpatterns = [
    # AboutUs URLs
    path("about/", AboutUsList.as_view(), name="about-list"),
    path("about/<int:pk>/", AboutUsDetail.as_view(), name="about-detail"),
    path("about/history/", AboutUsHistoryView.as_view(), name="about-history"),
    path("about/restore/<int:pk>/", AboutUsRestoreView.as_view(), name="about-restore"),

    # ContactUs URLs
    path("contact/", ContactUsList.as_view(), name="contact-list"),
    path("contact/<int:pk>/", ContactUsDetail.as_view(), name="contact-detail"),
    path("contact/history/", ContactUsHistoryView.as_view(), name="contact-history"),
    path("contact/restore/<int:pk>/", ContactUsRestoreView.as_view(), name="contact-restore"),

    # FAQ URLs
    path("faq/", FAQList.as_view(), name="faq-list"),
    path("faq/<int:pk>/", FAQDetail.as_view(), name="faq-detail"),
    path("faq/history/", FAQHistoryView.as_view(), name="faq-history"),
    path("faq/restore/<int:pk>/", FAQRestoreView.as_view(), name="faq-restore"),

    # LocationMap URLs
    path("location-map/", LocationMapListCreateView.as_view(), name="location-map-list"),
    path("location-map/<int:pk>/", LocationMapDetail.as_view(), name="location-map-detail"),
    path("location-map/history/", LocationMapHistoryView.as_view(), name="location-map-history"),
    path("location-map/restore/<int:pk>/", LocationMapRestoreView.as_view(), name="location-map-restore"),

    # TeamMember URLs
    path("team-member/", TeamMemberListCreateView.as_view(), name="team-member-list"),
    path("team-member/<int:pk>/", TeamMemberDetailView.as_view(), name="team-member-detail"),
    path("team-member/history/", TeamMemberHistoryView.as_view(), name="team-member-history"),
    path("team-member/restore/<int:pk>/", TeamMemberRestoreView.as_view(), name="team-member-restore"),

    # SiteStat URLs
    path("site-stat/", SiteStatListCreateView.as_view(), name="site-stat-list"),
    path("site-stat/<int:pk>/", SiteStatDetailView.as_view(), name="site-stat-detail"),
    path("site-stat/history/", SiteStatHistoryView.as_view(), name="site-stat-history"),
    path("site-stat/restore/<int:pk>/", SiteStatRestoreView.as_view(), name="site-stat-restore"),

    # TermsAndConditions URLs
    path("terms-and-conditions/", TermsAndConditionsListCreateView.as_view(), name="terms-and-conditions-list"),
    path("terms-and-conditions/<int:pk>/", TermsAndConditionsDetailView.as_view(), name="terms-and-conditions-detail"),
    path("terms-and-conditions/history/", TermsAndConditionsHistoryView.as_view(), name="terms-and-conditions-history"),
    path("terms-and-conditions/restore/<int:pk>/", TermsAndConditionsRestoreView.as_view(), name="terms-and-conditions-restore"),

    # PrivacyPolicy URLs
    path("privacy-policy/", PrivacyPolicyListCreateView.as_view(), name="privacy-policy-list"),
    path("privacy-policy/<int:pk>/", PrivacyPolicyDetailView.as_view(), name="privacy-policy-detail"),
    path("privacy-policy/history/", PrivacyPolicyHistoryView.as_view(), name="privacy-policy-history"),
    path("privacy-policy/restore/<int:pk>/", PrivacyPolicyRestoreView.as_view(), name="privacy-policy-restore"),
]
