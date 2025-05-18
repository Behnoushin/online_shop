# -------------------   Django imports ------------------------
from django.db import models
from django.utils import timezone
# -------------------   Apps imports ------------------------
from .validation import validate_company_phone_number, validate_version_format
from utility.models import BaseModel
from user_management.models import CustomUser 

##################################################################################
#                           AboutUs Model                                        #
##################################################################################

class AboutUs(BaseModel):
    title = models.CharField(max_length=150)
    content = models.TextField()

    def __str__(self):
        return "About Us"

##################################################################################
#                           ContactUs Model                                      #
##################################################################################

class ContactUs(BaseModel):
    email = models.EmailField()
    address = models.TextField()
    social_media_links = models.JSONField(unique=True, null=True, blank=True)
    working_hours = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(
        max_length=20, 
        validators=[validate_company_phone_number], 
        help_text="Enter only the last 8 digits of the company number (without 021)"
        )
    
    def save(self, *args, **kwargs):
        raw_phone = self.phone.strip()[-8:]
        self.phone = f"021{raw_phone}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "Contact Us"

##################################################################################
#                                FAQ Model                                       #
##################################################################################

class FAQ(BaseModel):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.question
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["question"], name="unique_faq_question")
        ]
    
##################################################################################
#                           LocationMap Model                                    #
##################################################################################

class LocationMap(BaseModel):
    title = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    map_embed_url = models.URLField()
    description = models.TextField(null=True, blank=True)
    added_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='location_maps'
        )

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["latitude", "longitude"], name="unique_location_coords")
        ]
        
##################################################################################
#                           TeamMember Model                                     #
##################################################################################

class TeamMember(BaseModel):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    social_links = models.JSONField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(
        max_length=20, 
        null=True, 
        blank=True, 
        validators=[validate_company_phone_number], 
        help_text="Enter only the last 8 digits of the number (without 021)"
        )

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "role"], name="unique_team_identity")
        ]
        
##################################################################################
#                           SiteStat Model                                       #
##################################################################################

class SiteStat(BaseModel):
    stat_name = models.CharField(max_length=100)
    stat_value = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='site_state_update'
        )

    def __str__(self):
        return f"{self.stat_name}: {self.stat_value}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["stat_name"], name="unique_stat_name")
        ]

##################################################################################
#                        TermsAndConditions Model                                #
##################################################################################

class TermsAndConditions(BaseModel):
    title = models.CharField(max_length=150)
    content = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    version = models.CharField(
        max_length=20,
        null=True, 
        blank=True, 
        validators=[validate_version_format]
        )

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "version"], name="unique_terms_version")
        ]

##################################################################################
#                           PrivacyPolicy Model                                  #
##################################################################################

class PrivacyPolicy(BaseModel):
    title = models.CharField(max_length=150)
    content = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    version = models.CharField(
        max_length=20,
        null=True, 
        blank=True, 
        validators=[validate_version_format]
        )

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "version"], name="unique_policy_version")
        ]