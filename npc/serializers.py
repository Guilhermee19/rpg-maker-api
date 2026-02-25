from rest_framework import serializers
from .models import NPC

class NPCSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPC
        fields = [
            'id', 'session', 'user', 'type', 'name', 'picture', 'life', 'note', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
