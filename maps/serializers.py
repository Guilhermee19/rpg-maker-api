from rest_framework import serializers
from .models import SessionMap

class SessionMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionMap
        fields = [
            "id",
            "session",
            "name",
            "image_url",
            "grid_enabled",
            "grid_size",
            "width",
            "height",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]