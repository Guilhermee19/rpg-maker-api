from rest_framework import serializers
from .models import Character, RPGSystem

class RPGSystemSerializer(serializers.ModelSerializer):
    """Serializer para RPGSystem model"""
    
    character_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = RPGSystem
        fields = [
            "id",
            "name", 
            "slug",
            "description",
            "base_sheet_data",
            "is_active",
            "is_default",
            "character_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "character_count"]
    
    def get_character_count(self, obj):
        """Retorna o número de personagens que usam este sistema"""
        return obj.characters.count()


class RPGSystemListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de sistemas"""
    
    class Meta:
        model = RPGSystem
        fields = [
            "id",
            "name", 
            "slug",
            "description",
            "is_active",
            "is_default",
        ]


class CharacterSerializer(serializers.ModelSerializer):
    """Serializer para Character model"""
    
    user_info = serializers.SerializerMethodField(read_only=True)
    system_name = serializers.CharField(read_only=True)
    rpg_system = RPGSystemListSerializer(read_only=True)
    
    class Meta:
        model = Character
        fields = [
            "id",
            "player_name", 
            "rpg_system",
            "system_name",
            "xp_total",
            "description",
            "avatar_url",
            "sheet_data",
            "is_active",
            "created_at",
            "updated_at",
            "user_info",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user_info", "rpg_system", "system_name"]
    
    def get_user_info(self, obj):
        """Retorna informações básicas do usuário"""
        if obj.user:
            return {
                'id': obj.user.id,
                'username': obj.user.username,
                'email': obj.user.email
            }
        return None
    
    def to_representation(self, instance):
        """Permite escrever rpg_system como slug ao criar/atualizar"""
        data = super().to_representation(instance)
        return data
    
    def create(self, validated_data):
        """Override create para aplicar template do sistema"""
        rpg_system = validated_data.get('rpg_system')
        
        # Se não foi fornecido um sistema, usa o padrão
        if not rpg_system:
            rpg_system = RPGSystem.get_default_system()
            validated_data['rpg_system'] = rpg_system
        
        # Se não foi fornecido sheet_data e tem sistema, usa o template do sistema
        if not validated_data.get('sheet_data') and rpg_system:
            validated_data['sheet_data'] = rpg_system.base_sheet_data
        
        return super().create(validated_data)


class CharacterCreateSerializer(serializers.ModelSerializer):
    """Serializer específico para criação de personagens"""
    
    rpg_system = serializers.PrimaryKeyRelatedField(
        queryset=RPGSystem.objects.filter(is_active=True), 
        required=False, 
        allow_null=True
    )
    
    class Meta:
        model = Character
        fields = [
            "player_name", 
            "rpg_system",
            "description",
            "avatar_url",
        ]
    
    def create(self, validated_data):
        """Cria personagem com template base do sistema"""
        rpg_system = validated_data.get('rpg_system')
        
        # Se não foi fornecido um sistema, usa o padrão
        if not rpg_system:
            rpg_system = RPGSystem.get_default_system()
            validated_data['rpg_system'] = rpg_system
        
        # Aplica o template base do sistema
        if rpg_system and rpg_system.base_sheet_data:
            validated_data['sheet_data'] = rpg_system.base_sheet_data
        
        return super().create(validated_data)