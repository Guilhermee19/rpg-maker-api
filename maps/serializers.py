from rest_framework import serializers
from .models import SessionMap
from session.models import Session

class SessionMapSerializer(serializers.ModelSerializer):
    session_name = serializers.CharField(source='session.name', read_only=True)
    session_master = serializers.CharField(source='session.master.username', read_only=True)
    
    class Meta:
        model = SessionMap
        fields = [
            "id",
            "session",
            "session_name",
            "session_master",
            "name",
            "image_url",
            "grid_enabled",
            "grid_size",
            "width",
            "height",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "session_name", "session_master"]
    
    def validate_session(self, value):
        """Valida se o usuário é membro da sessão"""
        user = self.context['request'].user
        if not value.members.filter(user=user).exists():
            raise serializers.ValidationError(
                "Você não tem acesso a esta sessão."
            )
        return value

class SessionMapCreateSerializer(serializers.ModelSerializer):
    """Serializer específico para criação de mapas"""
    
    class Meta:
        model = SessionMap
        fields = [
            "session",
            "name",
            "image_url",
            "grid_enabled",
            "grid_size",
            "width",
            "height",
        ]
    
    def validate_session(self, value):
        """Valida se o usuário é o mestre da sessão"""
        user = self.context['request'].user
        if value.master != user:
            raise serializers.ValidationError(
                "Apenas o mestre da sessão pode criar mapas."
            )
        return value

class SessionMapDetailSerializer(serializers.ModelSerializer):
    """Serializer detalhado para visualização de mapas"""
    session_info = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = SessionMap
        fields = [
            "id",
            "session",
            "session_info",
            "name",
            "image_url",
            "grid_enabled",
            "grid_size",
            "width",
            "height",
            "is_active",
            "created_at",
            "can_edit",
        ]
        read_only_fields = ["id", "created_at", "session_info", "can_edit"]
    
    def get_session_info(self, obj):
        return {
            'id': obj.session.id,
            'name': obj.session.name,
            'master': obj.session.master.username,
            'status': obj.session.status
        }
    
    def get_can_edit(self, obj):
        user = self.context['request'].user
        return obj.session.master == user