from django.db import models
from utility.models import BaseModel

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
    map_location = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return "Contact Us"

class FAQ(BaseModel):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.question