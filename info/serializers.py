# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import(
    AboutUs, ContactUs, FAQ, LocationMap,
    TeamMember, SiteStat,TermsAndConditions,
    PrivacyPolicy       
    )
from utility.serializers import BaseSerializer

##################################################################################
#                      AboutUsSerializer serializers                             #
##################################################################################

class AboutUsSerializer(BaseSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"

##################################################################################
#                    ContactUsSerializer serializers                             #
##################################################################################

class ContactUsSerializer(BaseSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"


##################################################################################
#                        FAQSerializer serializers                               #
##################################################################################

class FAQSerializer(BaseSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"
        

##################################################################################
#                    LocationMapSerializer serializers                           #
##################################################################################

class LocationMapSerializer(BaseSerializer):
    class Meta:
        model = LocationMap
        fields = "__all__"


##################################################################################
#                    TeamMemberSerializer serializers                            #
##################################################################################

class TeamMemberSerializer(BaseSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"


##################################################################################
#                     SiteStatSerializer serializers                             #
##################################################################################

class SiteStatSerializer(BaseSerializer):

    class Meta:
        model = SiteStat
        fields = "__all__"


##################################################################################
#                  TermsAndConditionsSerializer serializers                      #
##################################################################################

class TermsAndConditionsSerializer(BaseSerializer):
    class Meta:
        model = TermsAndConditions
        fields = "__all__"


##################################################################################
#                    PrivacyPolicySerializer serializers                         #
##################################################################################

class PrivacyPolicySerializer(BaseSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = "__all__"