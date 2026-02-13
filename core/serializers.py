from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - agora usado como perfil completo"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'date_joined', 'last_login', 'is_active'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


# ProfileSerializer removido - usando UserSerializer para perfis