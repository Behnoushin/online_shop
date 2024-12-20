from .models import UserProfile, PurchaseHistory, CustomUser
from .serializers import UserProfileSerializer, UserSerializer, PurchaseHistorySerializer, OTPSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from utility.views import BaseAPIView
from .permissions import IsStaffUser
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
import random


class UserRegistrationView(BaseAPIView, generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        phone_number = request.data.get("phone_number", None)
        age = request.data.get("age", None)

        if not username or not password or not email:
            return Response({"error": "تمام فیلدها اجباری هستند"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(username=username, password=password, email=email, phone_number=phone_number, age=age)
        
        UserProfile.objects.create(user=user)
        otp_code = random.randint(1000, 9999)
        user.otp_code = otp_code
        user.save()
        
        send_mail('OTP شما', f'کد تأیید شما: {otp_code}', [user.email])
        
        return Response({"message": "ثبت نام با موفقیت انجام شد. کد تأیید به ایمیل شما ارسال شد."}, status=status.HTTP_201_CREATED)


class UserLoginView(BaseAPIView, generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "نام کاربری یا رمز عبور اشتباه است"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(BaseAPIView, generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if user.is_authenticated:
            return UserProfile.objects.get(user=user)
        else:
            raise PermissionDenied("شما باید وارد حساب خود شوید تا به پروفایل دسترسی داشته باشید.")



class PurchaseHistoryView(BaseAPIView, generics.ListAPIView):
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsStaffUser]
    
    def get_queryset(self):
        return PurchaseHistory.objects.filter(user=self.request.user)


class PurchaseHistoryDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseHistory.objects.all()
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsStaffUser]
    
    
class OTPValidationView(BaseAPIView, generics.GenericAPIView):
    serializer_class = OTPSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']

        try:
            user = CustomUser.objects.get(email=email, otp_code=otp_code)
            
            if not user.is_active:
                user.is_active = True
                user.otp_code = None
                user.save()
                return Response({"message": "ایمیل تأیید شد و حساب کاربری فعال شد."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "کاربر قبلاً فعال شده است."}, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({"error": "کد تأیید یا ایمیل اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)            