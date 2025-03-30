from django.contrib import admin
from .models import(
    AboutUs, ContactUs, FAQ, LocationMap,
    TeamMember, SiteStat, TermsAndConditions, PrivacyPolicy
    )

class AdminAccessControl(admin.ModelAdmin):
    """
    Base class for restricting access to admins
    """
    
    def has_add_permission(self, request):
        return request.user.is_superuser 

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser 


class AboutUsAdmin(AdminAccessControl):
    list_display = ["id", "content", "created_at", "updated_at"]
    search_fields = ["content"]
    ordering = ["id"]
    list_filter = ["created_at"]
    list_editable = ["content"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20


class ContactUsAdmin(AdminAccessControl):
    list_display = ["id", "email", "phone", "address", "created_at"]
    search_fields = ["email", "phone"]
    ordering = ["id"]
    list_filter = ["email", "created_at"]
    list_editable = ["email", "phone"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20


class FAQAdmin(AdminAccessControl):
    list_display = ["id", "question", "answer", "created_at"]
    search_fields = ["question"]
    ordering = ["id"]
    list_filter = ["category", "created_at"]
    list_editable = ["answer"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20


class LocationMapAdmin(AdminAccessControl):
    list_display = ["id", "title", "address", "latitude", "longitude", "created_at"]
    search_fields = ["title", "address"]
    ordering = ["id"]
    list_filter = ["created_at"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20


class TeamMemberAdmin(AdminAccessControl):
    list_display = ["id", "name", "role", "email", "created_at"]
    search_fields = ["name", "role", "email"]
    ordering = ["id"]
    list_filter = ["created_at"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20


class SiteStatAdmin(AdminAccessControl):
    list_display = ["id", "stat_name", "stat_value", "description", "last_updated", "updated_by"]
    search_fields = ["stat_name"]
    ordering = ["id"]
    list_filter = ["last_updated"]
    list_editable = ["stat_value", "description"]
    readonly_fields = ["id", "last_updated"]
    date_hierarchy = 'last_updated'
    list_per_page = 20


class TermsAndConditionsAdmin(AdminAccessControl):
    list_display = ["id", "title", "start_date", "end_date", "created_at"]
    search_fields = ["title"]
    ordering = ["id"]
    list_filter = ["start_date", "end_date"]
    list_editable = ["title", "start_date", "end_date"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20


class PrivacyPolicyAdmin(AdminAccessControl):
    list_display = ["id", "title", "start_date", "end_date", "created_at"]
    search_fields = ["title"]
    ordering = ["id"]
    list_filter = ["start_date", "end_date"]
    list_editable = ["title", "start_date", "end_date"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20


admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(LocationMap, LocationMapAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(SiteStat, SiteStatAdmin)
admin.site.register(TermsAndConditions, TermsAndConditionsAdmin)
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
