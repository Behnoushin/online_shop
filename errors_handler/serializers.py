from rest_framework import serializers
from .models import ExceptionLog

class ExceptionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExceptionLog
        fields =  "__all__"
