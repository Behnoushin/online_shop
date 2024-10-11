from rest_framework import serializers
from .models import AppAdmin

class AppAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppAdmin
        fields = ['id', 'admin_username', 'created_at']
        