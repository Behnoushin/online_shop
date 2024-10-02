from django.db import models

class AboutUs(models.Model):
    content = models.TextField()

    def __str__(self):
        return "About Us"

class ContactUs(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return "Contact Us"

class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()

    def __str__(self):
        return self.question