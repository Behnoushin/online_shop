from django.db import models
from django.utils import timezone
from utility.models import BaseModel
from user_management.models import CustomUser 


class AboutUs(BaseModel):
    title = models.CharField(max_length=150)
    content = models.TextField()

    def __str__(self):
        return "About Us"


class ContactUs(BaseModel):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    social_media_links = models.JSONField(null=True, blank=True)
    working_hours = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return "Contact Us"


class FAQ(BaseModel):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.question
    
    
class LocationMap(BaseModel):
    title = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    map_embed_url = models.URLField()
    description = models.TextField(null=True, blank=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class TeamMember(BaseModel):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    social_links = models.JSONField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class SiteStat(BaseModel):
    stat_name = models.CharField(max_length=100)
    stat_value = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.stat_name}: {self.stat_value}"


class TermsAndConditions(BaseModel):
    title = models.CharField(max_length=150)
    content = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    version = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title


class PrivacyPolicy(BaseModel):
    title = models.CharField(max_length=150)
    content = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    version = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title
