# -------------------   Django imports ------------------------
from django_filters.rest_framework import DjangoFilterBackend
# -------------------  DRF imports   ------------------------
from rest_framework import generics, permissions
# -------------------   Apps imports ------------------------
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
from .permissions import ReadOnlyForAllButAdmin
from utility.views import BaseAPIView


# -----------------------------------------------------------------------------
# AboutUs Views
# -----------------------------------------------------------------------------

class AboutUsList(BaseAPIView, generics.ListCreateAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [ReadOnlyForAllButAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']
    search_fields = ['title', 'content']


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    search_fields = ['question', 'answer']


class FAQDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [ReadOnlyForAllButAdmin]

# -----------------------------------------------------------------------------
# LocationMap Views
# -----------------------------------------------------------------------------

class LocationMapListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = LocationMap.objects.all()
    serializer_class = LocationMapSerializer
    permission_classes = [ReadOnlyForAllButAdmin]


class LocationMapDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = LocationMap.objects.all()
    serializer_class = LocationMapSerializer
    permission_classes = [ReadOnlyForAllButAdmin]

# -----------------------------------------------------------------------------
# TeamMember Views
# -----------------------------------------------------------------------------

class TeamMemberListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'email']
    search_fields = ['name', 'role', 'bio']


class TeamMemberDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAdminUser]

# -----------------------------------------------------------------------------
# SiteStat Views
# -----------------------------------------------------------------------------

class SiteStatListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = SiteStat.objects.all()
    serializer_class = SiteStatSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)


class SiteStatDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = SiteStat.objects.all()
    serializer_class = SiteStatSerializer
    permission_classes = [permissions.IsAdminUser]

# -----------------------------------------------------------------------------
# TermsAndConditions Views
# -----------------------------------------------------------------------------

class TermsAndConditionsListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer
    permission_classes = [ReadOnlyForAllButAdmin]


class TermsAndConditionsDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer
    permission_classes = [ReadOnlyForAllButAdmin]

# -----------------------------------------------------------------------------
# PrivacyPolicy Views
# -----------------------------------------------------------------------------

class PrivacyPolicyListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    permission_classes = [ReadOnlyForAllButAdmin]


class PrivacyPolicyDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    permission_classes = [ReadOnlyForAllButAdmin]
