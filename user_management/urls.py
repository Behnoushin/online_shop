from django.urls import path
from .views import UserRegistrationView, UserProfileView, PurchaseHistoryView , PurchaseHistoryDetailView, OTPValidationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("purchasehistory/", PurchaseHistoryView.as_view(), name="purchase-history"),
    path("purchase-history/<int:pk>/", PurchaseHistoryDetailView.as_view(), name="purchase-history-detail"),
    path("validate-otp/", OTPValidationView.as_view(), name="validate-otp"),
]
