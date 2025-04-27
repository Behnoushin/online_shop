import re
import random

from .models import UserProfile, PurchaseHistory, CustomUser
from .serializers import UserProfileSerializer, UserSerializer, PurchaseHistorySerializer, ChangePasswordSerializer, EmailSerializer
from .permissions import IsStaffUser
from utility.views import BaseAPIView
from messaging.utils import get_formatted_message

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.cache import cache


# -----------------------------------------------------------------------------
# User Registration View
# -----------------------------------------------------------------------------

class UserRegistrationView(BaseAPIView, generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

    def send_email(self, subject, message, recipient):
        """
        Method to send email to user
        """
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,  
                recipient_list=[recipient]
            )
        except Exception as e:
            print(f"خطا در ارسال ایمیل: {e}") 


    def create(self, request, *args, **kwargs):
        """
        Registers a new user, creates a profile, generates an OTP, and sends a confirmation email.
        """
        data = request.data
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
        
        otp_message = get_formatted_message("otp_message", otp_code=otp_code)
        
        welcome_message = get_formatted_message("welcome_message", username=username)

        email_content = f"{welcome_message}\n\n{otp_message}"

        self.send_email("ثبت‌نام شما با موفقیت انجام شد", email_content, user.email)
        
        return Response({"message": "ثبت نام با موفقیت انجام شد. کد تأیید به ایمیل شما ارسال شد."}, status=status.HTTP_201_CREATED)


# -----------------------------------------------------------------------------
# User Login View
# -----------------------------------------------------------------------------

class UserLoginView(BaseAPIView, generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """
        Authenticates the user and returns JWT tokens if the login is successful.
        """
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


# -----------------------------------------------------------------------------
# User Profile View
# -----------------------------------------------------------------------------

class UserProfileView(BaseAPIView, generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Returns the profile of the authenticated user.
        """
        user = self.request.user
        if user.is_authenticated:
            
            try:
                return UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                raise PermissionDenied("پروفایل کاربری برای شما ایجاد نشده است.")
            
        else:
            raise PermissionDenied("شما باید وارد حساب خود شوید تا به پروفایل دسترسی داشته باشید.")


# -----------------------------------------------------------------------------
# User Profile Update View
# -----------------------------------------------------------------------------

class UserProfileUpdateView(BaseAPIView, generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        This method returns the authenticated user's object to be updated.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        
        # Update first name and last name
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        
        # Update email
        if 'email' in request.data:
            user.email = request.data['email']
        
        # Update phone number and fixed phone number
        if 'phone_number' in request.data:
            user.phone_number = request.data['phone_number']
        if 'fixed_phone' in request.data:
            user.fixed_phone = request.data['fixed_phone']
        
        # Update age
        if 'age' in request.data:
            user.age = request.data['age']
        
        user.save()
        return Response({"message": "اطلاعات شما با موفقیت به روزرسانی شد."}, status=status.HTTP_200_OK)


# -----------------------------------------------------------------------------
# Change Password View
# -----------------------------------------------------------------------------

class ChangePasswordView(BaseAPIView, generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        This method returns the authenticated user object for password update.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')

        # Check that the old password, new password, and confirm new password are provided
        if not old_password or not new_password or not confirm_new_password:
            raise ValidationError({"error": "تمامی فیلدهای رمز عبور باید پر شوند."})

        # Check that the new password is at least 8 characters long
        if len(new_password) < 8:
            raise ValidationError({"error": "رمز عبور جدید باید حداقل ۸ کاراکتر داشته باشد."})

        # Check that the new password contains at least one number
        if not re.search(r'\d', new_password):
            raise ValidationError({"error": "رمز عبور جدید باید حاوی حداقل یک عدد باشد."})

        # Check that the new password contains at least one uppercase letter
        if not re.search(r'[A-Z]', new_password):
            raise ValidationError({"error": "رمز عبور جدید باید حاوی حداقل یک حرف بزرگ انگلیسی باشد."})

        # Check that the new password contains at least one lowercase letter
        if not re.search(r'[a-z]', new_password):
            raise ValidationError({"error": "رمز عبور جدید باید حاوی حداقل یک حرف کوچک انگلیسی باشد."})

        # Check that the new password and confirm new password match
        if new_password != confirm_new_password:
            raise ValidationError({"error": "رمز عبور جدید و تأیید رمز عبور یکسان نیستند."})

        # Check the old password
        if not user.check_password(old_password):
            return Response({"error": "رمز عبور قبلی صحیح نیست."}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(new_password)
        user.save()

        return Response({"message": "پسورد شما با موفقیت تغییر یافت."}, status=status.HTTP_200_OK)


# -----------------------------------------------------------------------------
# Purchase History View
# -----------------------------------------------------------------------------

class PurchaseHistoryView(BaseAPIView, generics.ListAPIView):
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsStaffUser]
    
    def get_queryset(self):
        """
        Filters purchase history based on the delivery status (if provided).
        """
        queryset = PurchaseHistory.objects.filter(user=self.request.user)
        is_delivered = self.request.query_params.get("is_delivered")
        
        if is_delivered is not None:
            queryset = queryset.filter(is_delivered=is_delivered.lower() == "true")
        return queryset


class PurchaseHistoryDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseHistory.objects.all()
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsStaffUser]
    
    def patch(self, request, *args, **kwargs):
        """
        Updates the delivery status of a specific purchase history record.
        """
        instance = self.get_object()
        
        if 'is_delivered' in request.data:
            instance.is_delivered = request.data['is_delivered']
            instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    
# -----------------------------------------------------------------------------
# OTP Validation View
# -----------------------------------------------------------------------------

class SendOTPView(BaseAPIView, generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        """
        Generates and sends an OTP, saves it in cache with a timeout.
        """
        # Step 1: Validate the incoming request data using the serializer
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Get the email from the validated data (This is where the problem was)
        email = serializer.validated_data['email']

        # Step 3: Check if there is an existing valid OTP for this email
        cache_key = f"otp_{email}"
        existing_otp = cache.get(cache_key)
        if existing_otp:
            return Response({"error": "کد تأیید قبلی هنوز معتبر است. لطفاً کمی صبر کنید."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Step 4: Generate a new 6-digit OTP
        otp_code = random.randint(100000, 999999)

        # Step 5: Save the OTP in cache with a timeout (e.g., 2 minutes)
        cache.set(cache_key, otp_code, timeout=120)

        # Step 6: Send the OTP (currently just printing; replace with actual email sending in production)
        print(f"Sending OTP {otp_code} to {email}")

        return Response({"message": "کد تأیید با موفقیت ارسال شد."}, status=status.HTTP_200_OK)
