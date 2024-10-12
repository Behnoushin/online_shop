from django.db import models
from utility.models import BaseModel
from utility.models import SoftDeleteManager

class AboutUs(BaseModel):
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()


    def __str__(self):
        return "About Us"

class ContactUs(BaseModel):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()
    
    def __str__(self):
        return "Contact Us"

class FAQ(BaseModel):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()

    def __str__(self):
        return self.question