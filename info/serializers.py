# -------------------  DRF imports  ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import (
    AboutUs, ContactUs, FAQ, LocationMap,
    TeamMember, SiteStat, TermsAndConditions,
    PrivacyPolicy
)
from utility.serializers import BaseSerializer

##################################################################################
#                      AboutUsSerializer serializers                             #
##################################################################################

class AboutUsSerializer(BaseSerializer):
    """
    Serializer for AboutUs model, includes history and soft-delete fields.
    """
    class Meta:
        model = AboutUs
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "is_deleted", "deleted_at", "history")

    def validate(self, data):
        """
        Ensures that 'social_media_links' has at least 3 characters.
        """
        social_links = data.get("social_media_links")
        if social_links and len(social_links) < 3:
            raise serializers.ValidationError("Social media links must contain at least 3 characters.")
        return data

##################################################################################
#                    ContactUsSerializer serializers                             #
##################################################################################

class ContactUsSerializer(BaseSerializer):
    """
    Serializer for ContactUs model with validation, history, and soft-delete support.
    """
    class Meta:
        model = ContactUs
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "is_deleted", "deleted_at", "history")

    def validate(self, data):
        """
        Validates that 'message' contains at least 10 characters.
        """
        message = data.get("message")
        if message and len(message.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long.")
        return data

##################################################################################
#                        FAQSerializer serializers                               #
##################################################################################

class FAQSerializer(BaseSerializer):
    """
    Serializer for FAQ model, includes category indexing and history.
    """
    class Meta:
        model = FAQ
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "is_deleted", "deleted_at", "history")

    def validate(self, data):
        """
        Checks that both 'question' and 'answer' fields are provided.
        """
        if not data.get("question") or not data.get("answer"):
            raise serializers.ValidationError("Both question and answer are required.")
        return data
    
##################################################################################
#                    LocationMapSerializer serializers                           #
##################################################################################

class LocationMapSerializer(BaseSerializer):
    """
    Serializer for LocationMap model, includes coordinates uniqueness and history.
    """
    class Meta:
        model = LocationMap
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "is_deleted", "deleted_at", "history")


##################################################################################
#                    TeamMemberSerializer serializers                            #
##################################################################################

class TeamMemberSerializer(BaseSerializer):
    """
    Serializer for TeamMember model, includes unique name-role validation and history.
    """
    class Meta:
        model = TeamMember
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "is_deleted", "deleted_at", "history")


##################################################################################
#                     SiteStatSerializer serializers                             #
##################################################################################

class SiteStatSerializer(BaseSerializer):
    """
    Serializer for SiteStat model, includes stat_name uniqueness and history.
    """
    class Meta:
        model = SiteStat
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "is_deleted", "deleted_at", "history")

    def validate(self, data):
        """
        Ensures that 'value' is not negative.
        """
        value = data.get("value")
        if value is not None and value < 0:
            raise serializers.ValidationError("Statistic value cannot be negative.")
        return data

##################################################################################
#                  TermsAndConditionsSerializer serializers                      #
##################################################################################

class TermsAndConditionsSerializer(BaseSerializer):
    """
    Serializer for TermsAndConditions model with version control and history.
    """
    class Meta:
        model = TermsAndConditions
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "is_deleted", "deleted_at", "history")

    def validate(self, data):
        """
        Validates that 'end_date' is later than 'start_date'.
        """
        start = data.get("start_date")
        end = data.get("end_date")
        if start and end and end < start:
            raise serializers.ValidationError("End date must be after start date.")
        return data

##################################################################################
#                    PrivacyPolicySerializer serializers                         #
##################################################################################

class PrivacyPolicySerializer(BaseSerializer):
    """
    Serializer for PrivacyPolicy model with versioning and history.
    """
    class Meta:
        model = PrivacyPolicy
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "is_deleted", "deleted_at", "history")

    def validate(self, data):
        """
        Validates that 'end_date' is later than 'start_date'.
        """
        start = data.get("start_date")
        end = data.get("end_date")
        if start and end and end < start:
            raise serializers.ValidationError("End date must be after start date.")
        return data
    