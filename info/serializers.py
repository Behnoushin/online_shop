from rest_framework import serializers
from .models import(
    AboutUs, ContactUs, FAQ, LocationMap,
    TeamMember, SiteStat,TermsAndConditions,
    PrivacyPolicy       
    )
from user_management.models import CustomUser
from utility.serializers import BaseSerializer


class AboutUsSerializer(BaseSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"


class ContactUsSerializer(BaseSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"


class FAQSerializer(BaseSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"
        

class LocationMapSerializer(BaseSerializer):
    class Meta:
        model = LocationMap
        fields = "__all__"


class TeamMemberSerializer(BaseSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"


class SiteStatSerializer(BaseSerializer):
    updated_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False) #I did this because I wanted to include the updated_by field in the serializer to store and retrieve the user who updated the SiteStat.

    class Meta:
        model = SiteStat
        fields = "__all__"


class TermsAndConditionsSerializer(BaseSerializer):
    class Meta:
        model = TermsAndConditions
        fields = "__all__"


class PrivacyPolicySerializer(BaseSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = "__all__"