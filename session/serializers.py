from rest_framework import serializers
from .models import Session, SessionMember, SessionInvite, SessionCharacter
from characters.serializers import CharacterSerializer
from maps.serializers import SessionMapSerializer
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
    character = CharacterSerializer(read_only=True)
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = SessionCharacter
        fields = ['id', 'user', 'character', 'joined_at']


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
    maps = SessionMapSerializer(many=True, read_only=True)
    total_members = serializers.SerializerMethodField()
    total_characters = serializers.SerializerMethodField()
    total_maps = serializers.SerializerMethodField()
    
    class Meta:
        model = Session
        fields = ['id', 'master', 'name', 'description', 'system_key', 'status', 
                 'created_at', 'updated_at', 'members', 'session_characters', 
                 'invites', 'maps', 'total_members', 'total_characters', 'total_maps']
    
    def get_total_members(self, obj):
        return obj.members.count()
    
    def get_total_characters(self, obj):
        return obj.session_characters.count()
    
    def get_total_maps(self, obj):
        return obj.maps.count()


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"
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