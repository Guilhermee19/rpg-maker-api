from rest_framework import serializers
from .models import Character

class CharacterSerializer(serializers.ModelSerializer):
    """Serializer para Character model"""
    
    user_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Character
        fields = [
            "id",
            "player_name", 
            "system_key",
            "xp_total",
            "description",
            "avatar_url",
            "sheet_data",
            "is_active",
            "created_at",
            "updated_at",
            "user_info",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user_info"]
    
    def get_user_info(self, obj):
        """Retorna informações básicas do usuário"""
        if obj.user:
            return {
                'id': obj.user.id,
                'username': obj.user.username,
                'email': obj.user.email
            }
        return None