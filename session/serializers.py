from rest_framework import serializers
from .models import Session, SessionMember, SessionInvite, SessionCharacter


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