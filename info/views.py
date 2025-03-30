from .models import(
    AboutUs, ContactUs, FAQ, LocationMap,
    TeamMember, SiteStat, TermsAndConditions,
    PrivacyPolicy
    )
from .serializers import(
    AboutUsSerializer, ContactUsSerializer, FAQSerializer,
    LocationMapSerializer, TeamMemberSerializer, SiteStatSerializer,
    TermsAndConditionsSerializer, PrivacyPolicySerializer
    )
from utility.views import BaseAPIView
from rest_framework import generics, permissions


class ReadOnlyForAllButAdmin(permissions.BasePermission):
    """
    All users (even unauthenticated ones) can view the data,
    but only admins are allowed to create, update, or delete.
    """
    def has_permission(self, request, view):
        # Allow all GET (read-only) requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only admins can modify the data
        return request.user and request.user.is_staff


# -----------------------------------------------------------------------------
# AboutUs Views
# -----------------------------------------------------------------------------

class AboutUsList(BaseAPIView, generics.ListCreateAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [ReadOnlyForAllButAdmin]


class AboutUsDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [ReadOnlyForAllButAdmin]

# -----------------------------------------------------------------------------
# ContactUs Views
# -----------------------------------------------------------------------------

class ContactUsList(BaseAPIView, generics.ListCreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [ReadOnlyForAllButAdmin]


class ContactUsDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [ReadOnlyForAllButAdmin]

# -----------------------------------------------------------------------------
# FAQ Views
# -----------------------------------------------------------------------------

class FAQList(BaseAPIView, generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [ReadOnlyForAllButAdmin]


class FAQDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [ReadOnlyForAllButAdmin]

# -----------------------------------------------------------------------------
# LocationMap Views
# -----------------------------------------------------------------------------

class LocationMapListCreateView(generics.ListCreateAPIView):
    queryset = LocationMap.objects.all()
    serializer_class = LocationMapSerializer
    permission_classes = [ReadOnlyForAllButAdmin]


class LocationMapDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LocationMap.objects.all()
    serializer_class = LocationMapSerializer
    permission_classes = [ReadOnlyForAllButAdmin]

# -----------------------------------------------------------------------------
# TeamMember Views
# -----------------------------------------------------------------------------

class TeamMemberListCreateView(generics.ListCreateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [ReadOnlyForAllButAdmin]


class TeamMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [ReadOnlyForAllButAdmin]

# -----------------------------------------------------------------------------
# SiteStat Views
# -----------------------------------------------------------------------------

class SiteStatListCreateView(generics.ListCreateAPIView):
    queryset = SiteStat.objects.all()
    serializer_class = SiteStatSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)


class SiteStatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SiteStat.objects.all()
    serializer_class = SiteStatSerializer
    permission_classes = [permissions.IsAdminUser]

# -----------------------------------------------------------------------------
# TermsAndConditions Views
# -----------------------------------------------------------------------------

class TermsAndConditionsListCreateView(generics.ListCreateAPIView):
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer
    permission_classes = [ReadOnlyForAllButAdmin]


class TermsAndConditionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer
    permission_classes = [ReadOnlyForAllButAdmin]

# -----------------------------------------------------------------------------
# PrivacyPolicy Views
# -----------------------------------------------------------------------------

class PrivacyPolicyListCreateView(generics.ListCreateAPIView):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    permission_classes = [ReadOnlyForAllButAdmin]


class PrivacyPolicyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    permission_classes = [ReadOnlyForAllButAdmin]
