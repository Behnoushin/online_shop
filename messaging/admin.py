from django.contrib import admin
from .models import Template

class TemplateAdmin(admin.ModelAdmin):
    list_display = ('slug', 'text')
    search_fields = ('slug', 'text')
    list_filter = ('slug', 'text')
    
    
admin.site.register(Template, TemplateAdmin)
