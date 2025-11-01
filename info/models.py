# -------------------   Django imports ------------------------
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

# -------------------   Apps imports ------------------------
from .validation import validate_company_phone_number, validate_version_format
from utility.models import BaseModel
from user_management.models import CustomUser

##################################################################################
#                           AboutUs Model                                        #
##################################################################################

class AboutUs(BaseModel):
    """
    Model for storing information about the company.
    """
    title = models.CharField(max_length=150, help_text="Title of the About Us section")
    content = models.TextField(help_text="Content of the About Us section")

    history = HistoricalRecords()

    def __str__(self):
        return f"AboutUs: {self.title}"

    def __repr__(self):
        return f"<AboutUs(id={self.id}, title='{self.title}')>"

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"
        indexes = [
            models.Index(fields=["title"], name="aboutus_title_idx")
        ]
        ordering = ["created_at"]


##################################################################################
#                           ContactUs Model                                      #
##################################################################################

class ContactUs(BaseModel):
    """
    Model for storing company's contact information.
    """
    email = models.EmailField(help_text="Company contact email")
    address = models.TextField(help_text="Company address")
    social_media_links = models.JSONField(unique=True, null=True, blank=True, help_text="Social media links")
    working_hours = models.CharField(max_length=100, null=True, blank=True, help_text="Working hours")
    phone = models.CharField(
        max_length=20,
        validators=[validate_company_phone_number],
        help_text="Enter only the last 8 digits of the company number (without 021)"
    )

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        raw_phone = self.phone.strip()[-8:]
        self.phone = f"021{raw_phone}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ContactUs: {self.email}"

    def __repr__(self):
        return f"<ContactUs(id={self.id}, email='{self.email}')>"

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"
        indexes = [
            models.Index(fields=["email"], name="contactus_email_idx"),
            models.Index(fields=["phone"], name="contactus_phone_idx")
        ]
        ordering = ["created_at"]


##################################################################################
#                                FAQ Model                                       #
##################################################################################

class FAQ(BaseModel):
    """
    Model for storing frequently asked questions.
    """
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.question

    def __repr__(self):
        return f"<FAQ(id={self.id}, question='{self.question[:50]}')>"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["question"], name="unique_faq_question")
        ]
        indexes = [
            models.Index(fields=["category"], name="faq_category_idx")
        ]
        ordering = ["created_at"]


##################################################################################
#                           LocationMap Model                                    #
##################################################################################

class LocationMap(BaseModel):
    """
    Model for storing location map data.
    """
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

    history = HistoricalRecords()

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<LocationMap(id={self.id}, title='{self.title}')>"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["latitude", "longitude"], name="unique_location_coords")
        ]
        indexes = [
            models.Index(fields=["title"], name="locationmap_title_idx")
        ]
        ordering = ["created_at"]


##################################################################################
#                           TeamMember Model                                     #
##################################################################################

class TeamMember(BaseModel):
    """
    Model for storing team members.
    """
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

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<TeamMember(id={self.id}, name='{self.name}', role='{self.role}')>"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "role"], name="unique_team_identity")
        ]
        indexes = [
            models.Index(fields=["role"], name="teammember_role_idx")
        ]
        ordering = ["name"]


##################################################################################
#                           SiteStat Model                                       #
##################################################################################

class SiteStat(BaseModel):
    """
    Model for storing site statistics.
    """
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

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.stat_name}: {self.stat_value}"

    def __repr__(self):
        return f"<SiteStat(id={self.id}, stat_name='{self.stat_name}', value={self.stat_value})>"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["stat_name"], name="unique_stat_name")
        ]
        indexes = [
            models.Index(fields=["stat_name"], name="sitestat_name_idx")
        ]
        ordering = ["stat_name"]


##################################################################################
#                        TermsAndConditions Model                                #
##################################################################################

class TermsAndConditions(BaseModel):
    """
    Model for storing Terms and Conditions with version control.
    """
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

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.title} ({self.version})"

    def __repr__(self):
        return f"<TermsAndConditions(id={self.id}, title='{self.title}', version='{self.version}')>"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "version"], name="unique_terms_version")
        ]
        indexes = [
            models.Index(fields=["title"], name="terms_title_idx"),
            models.Index(fields=["version"], name="terms_version_idx")
        ]
        ordering = ["start_date"]


##################################################################################
#                           PrivacyPolicy Model                                  #
##################################################################################

class PrivacyPolicy(BaseModel):
    """
    Model for storing Privacy Policies with versioning.
    """
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

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.title} ({self.version})"

    def __repr__(self):
        return f"<PrivacyPolicy(id={self.id}, title='{self.title}', version='{self.version}')>"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "version"], name="unique_policy_version")
        ]
        indexes = [
            models.Index(fields=["title"], name="policy_title_idx"),
            models.Index(fields=["version"], name="policy_version_idx")
        ]
        ordering = ["start_date"]
