from rest_framework import serializers
from .models import Session, SessionMember, SessionInvite, SessionCharacter
from django.contrib.auth import get_user_model

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class SessionMemberDetailSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = SessionMember
        fields = ['id', 'user', 'role', 'joined_at']


class SessionCharacterDetailSerializer(serializers.ModelSerializer):
    character = serializers.SerializerMethodField()
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = SessionCharacter
        fields = ['id', 'user', 'character', 'joined_at']
    
    def get_character(self, obj):
        """Lazy import para evitar circular dependency"""
        from characters.serializers import CharacterSerializer
        return CharacterSerializer(obj.character, context=self.context).data


class SessionInviteDetailSerializer(serializers.ModelSerializer):
    is_valid = serializers.ReadOnlyField()
    invite_link = serializers.SerializerMethodField()
    
    class Meta:
        model = SessionInvite
        fields = ['id', 'code', 'max_uses', 'uses_count', 'expires_at', 
                 'created_at', 'is_valid', 'invite_link']
    
    def get_invite_link(self, obj):
        # Você pode ajustar este link conforme sua estrutura de frontend
        request = self.context.get('request')
        if request:
            base_url = request.build_absolute_uri('/')
            return f"{base_url}join/{obj.code}"
        return f"/join/{obj.code}"


class SessionDetailSerializer(serializers.ModelSerializer):
    master = UserBasicSerializer(read_only=True)
    members = SessionMemberDetailSerializer(many=True, read_only=True)
    session_characters = SessionCharacterDetailSerializer(many=True, read_only=True)
    invites = SessionInviteDetailSerializer(many=True, read_only=True)
    maps = serializers.SerializerMethodField()  # Mudança para SerializerMethodField
    total_members = serializers.SerializerMethodField()
    total_characters = serializers.SerializerMethodField()
    total_maps = serializers.SerializerMethodField()
    
    class Meta:
        model = Session
        fields = ['id', 'master', 'name', 'description', 'status', 
                 'created_at', 'updated_at', 'members', 'session_characters', 
                 'invites', 'maps', 'total_members', 'total_characters', 'total_maps']
    
    def get_maps(self, obj):
        """Retorna mapas da sessão - import lazy para evitar circular"""
        try:
            # Import lazy do SessionMapSerializer
            from maps.serializers import SessionMapSerializer
            maps = obj.maps.all()
            return SessionMapSerializer(maps, many=True, context=self.context).data
        except ImportError:
            # Fallback caso haja problemas de import
            return []
    
    def get_total_members(self, obj):
        return obj.members.count()
    
    def get_total_characters(self, obj):
        return obj.session_characters.count()
    
    def get_total_maps(self, obj):
        return obj.maps.count()


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["id", "master", "name", "description", "status", "created_at", "updated_at"]
        read_only_fields = ("id", "master", "created_at", "updated_at")


class SessionMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionMember
        fields = "__all__"


class SessionInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionInvite
        fields = "__all__"
        read_only_fields = ("id", "uses_count", "created_at")


class SessionCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionCharacter
        fields = "__all__"