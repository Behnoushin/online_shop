from django.contrib import admin
from .models import AboutUs, ContactUs, FAQ

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ["id", "content","created_at", "updated_at"]
    search_fields = ["content"]
    ordering = ["id"]
    list_filter = ["created_at"]
    list_editable = ["content"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "phone", "address", "created_at"]
    search_fields = ["email", "phone"]
    ordering = ["id"]
    list_filter = ["email", "created_at"]
    list_editable = ["email", "phone"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20

class FAQAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "answer", "created_at"]
    search_fields = ["question"]
    ordering = ["id"]
    list_filter = ["category", "created_at"]
    list_editable = ["answer"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20
    
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(FAQ, FAQAdmin)