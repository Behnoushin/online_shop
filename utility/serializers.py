from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):
    is_deleted = serializers.BooleanField(read_only=True)
    class Meta:
        abstract = True
        fields = ['id', 'created_at', 'updated_at', 'is_deleted'] 