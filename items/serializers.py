from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    session_name = serializers.CharField(source='session.name', read_only=True)

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['id', 'session_name']

    def validate_session(self, value):
        user = self.context['request'].user
        if value.master == user:
            return value
        if value.members.filter(user=user).exists():
            return value
        raise serializers.ValidationError(
            "Você não tem acesso a esta sessão."
        )