from django.contrib import admin
from .models import AboutUs, ContactUs, FAQ

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ["id", "content"]
    search_fields = ["content"]


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "phone", "address"]
    search_fields = ["email", "phone"]


class FAQAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "answer"]
    search_fields = ["question"]
    
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(FAQ, FAQAdmin)