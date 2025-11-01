# -------------------   Django imports ------------------------
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend

# -------------------  DRF imports   ------------------------
from rest_framework import generics, permissions, status
from rest_framework.response import Response

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
from utility.mixins import RestoreMixin

# -------------------------------------------------------------------
# Shared Cache TTL
# -------------------------------------------------------------------
CACHE_TTL = getattr(settings, "CACHE_TTL", 60 * 5)


# -------------------------------------------------------------------
# Base Info View
# -------------------------------------------------------------------
class BaseInfoView(BaseAPIView):
    """
    Base API view for info app.
    Provides cache support and shared attributes.
    """
    permission_classes = [ReadOnlyForAllButAdmin]


# -------------------------------------------------------------------
# Generic History & Restore Views
# -------------------------------------------------------------------
class GenericHistoryView(generics.ListAPIView):
    """
    List all historical changes for a model.
    Admin-only access.
    """
    permission_classes = [permissions.IsAdminUser]
    model = None 

    def get_queryset(self):
        return self.model.history.all()


class GenericRestoreView(RestoreMixin, generics.GenericAPIView):
    """
    Restore a soft-deleted record for a model.
    Admin-only access.
    """
    permission_classes = [permissions.IsAdminUser]
    serializer_class = None
    model = None  

    def post(self, request, pk):
        instance = self.model.objects.get(pk=pk)
        self.perform_restore(instance)
        return Response({"detail": "Record restored successfully."}, status=status.HTTP_200_OK)


# -----------------------------------------------------------------------------
# AboutUs Views
# -----------------------------------------------------------------------------
@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class AboutUsList(BaseInfoView, generics.ListCreateAPIView):
    """
    List and create AboutUs records.
    Supports filtering and public read access.
    """
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']
    search_fields = ['title', 'content']


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class AboutUsDetail(BaseInfoView, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an AboutUs record.
    Read-only for non-admin users.
    """
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer


class AboutUsHistoryView(GenericHistoryView):
    model = AboutUs


class AboutUsRestoreView(GenericRestoreView):
    model = AboutUs
    serializer_class = AboutUsSerializer


# -----------------------------------------------------------------------------
# ContactUs Views
# -----------------------------------------------------------------------------
@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class ContactUsList(BaseInfoView, generics.ListCreateAPIView):
    """
    List and create ContactUs records.
    Admin-only write, public read access.
    """
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class ContactUsDetail(BaseInfoView, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a ContactUs record.
    Read-only for non-admin users.
    """
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer


class ContactUsHistoryView(GenericHistoryView):
    model = ContactUs


class ContactUsRestoreView(GenericRestoreView):
    model = ContactUs
    serializer_class = ContactUsSerializer


# -----------------------------------------------------------------------------
# FAQ Views
# -----------------------------------------------------------------------------
@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class FAQList(BaseInfoView, generics.ListCreateAPIView):
    """
    List and create FAQ records.
    Supports searching and filtering.
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    search_fields = ['question', 'answer']


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class FAQDetail(BaseInfoView, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an FAQ record.
    Admin-only write access.
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class FAQHistoryView(GenericHistoryView):
    model = FAQ


class FAQRestoreView(GenericRestoreView):
    model = FAQ
    serializer_class = FAQSerializer

# -----------------------------------------------------------------------------
# LocationMap Views
# -----------------------------------------------------------------------------
@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class LocationMapListCreateView(BaseInfoView, generics.ListCreateAPIView):
    """
    List and create LocationMap records.
    Admin-only write, public read access.
    """
    queryset = LocationMap.objects.all()
    serializer_class = LocationMapSerializer


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class LocationMapDetail(BaseInfoView, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a LocationMap record.
    Read-only for non-admin users.
    """
    queryset = LocationMap.objects.all()
    serializer_class = LocationMapSerializer


class LocationMapHistoryView(GenericHistoryView):
    model = LocationMap


class LocationMapRestoreView(GenericRestoreView):
    model = LocationMap
    serializer_class = LocationMapSerializer


# -----------------------------------------------------------------------------
# TeamMember Views
# -----------------------------------------------------------------------------
@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class TeamMemberListCreateView(BaseInfoView, generics.ListCreateAPIView):
    """
    List and create TeamMember records.
    Admin-only access with search and filter.
    """
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'email']
    search_fields = ['name', 'role', 'bio']


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class TeamMemberDetailView(BaseInfoView, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a TeamMember record.
    Admin-only access.
    """
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAdminUser]


class TeamMemberHistoryView(GenericHistoryView):
    model = TeamMember


class TeamMemberRestoreView(GenericRestoreView):
    model = TeamMember
    serializer_class = TeamMemberSerializer


# -----------------------------------------------------------------------------
# SiteStat Views
# -----------------------------------------------------------------------------
@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class SiteStatListCreateView(BaseInfoView, generics.ListCreateAPIView):
    """
    List and create SiteStat records.
    Admin-only access, saves updated_by user.
    """
    queryset = SiteStat.objects.all()
    serializer_class = SiteStatSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class SiteStatDetailView(BaseInfoView, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a SiteStat record.
    Admin-only access.
    """
    queryset = SiteStat.objects.all()
    serializer_class = SiteStatSerializer
    permission_classes = [permissions.IsAdminUser]


class SiteStatHistoryView(GenericHistoryView):
    model = SiteStat


class SiteStatRestoreView(GenericRestoreView):
    model = SiteStat
    serializer_class = SiteStatSerializer


# -----------------------------------------------------------------------------
# TermsAndConditions Views
# -----------------------------------------------------------------------------
@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class TermsAndConditionsListCreateView(BaseInfoView, generics.ListCreateAPIView):
    """
    List and create TermsAndConditions records.
    Supports public read and admin write.
    """
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class TermsAndConditionsDetailView(BaseInfoView, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a TermsAndConditions record.
    Read-only for non-admin users.
    """
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer


class TermsAndConditionsHistoryView(GenericHistoryView):
    model = TermsAndConditions


class TermsAndConditionsRestoreView(GenericRestoreView):
    model = TermsAndConditions
    serializer_class = TermsAndConditionsSerializer


# -----------------------------------------------------------------------------
# PrivacyPolicy Views
# -----------------------------------------------------------------------------
@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class PrivacyPolicyListCreateView(BaseInfoView, generics.ListCreateAPIView):
    """
    List and create PrivacyPolicy records.
    Supports public read and admin write.
    """
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class PrivacyPolicyDetailView(BaseInfoView, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a PrivacyPolicy record.
    Read-only for non-admin users.
    """
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer


class PrivacyPolicyHistoryView(GenericHistoryView):
    model = PrivacyPolicy


class PrivacyPolicyRestoreView(GenericRestoreView):
    model = PrivacyPolicy
    serializer_class = PrivacyPolicySerializer
