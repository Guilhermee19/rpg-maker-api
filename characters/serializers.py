from rest_framework import serializers
from .models import Character, RPGSystem


class RPGSystemSerializer(serializers.ModelSerializer):
    """Serializer para RPGSystem model"""
    
    character_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = RPGSystem
        fields = [
            "slug",
            "name", 
            "logo_url", 
            "description",
            "base_sheet_data",
            "is_active",
            "is_default",
            "character_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "created_at", "updated_at", "character_count"]
    
    def get_character_count(self, obj):
        """Retorna o número de personagens que usam este sistema"""
        return obj.characters.count()


class RPGSystemListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de sistemas"""
    
    class Meta:
        model = RPGSystem
        fields = [
            "slug",
            "name", 
            'logo_url',
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


class CharacterCreateSerializer(serializers.ModelSerializer):
    """Serializer específico para criação de personagens"""
    
    # slug é a PK do RPGSystem
    rpg_system = serializers.SlugRelatedField(
        slug_field='slug',
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
        """
        Cria personagem garantindo que o sheet_data venha do base_sheet_data
        do rpg_system selecionado. O Character.save() cuida disso, mas forçamos
        aqui também para garantir consistência mesmo sem passar pelo save().
        """
        rpg_system = validated_data.get('rpg_system')

        # Se não foi fornecido um sistema, usa o padrão
        if not rpg_system:
            rpg_system = RPGSystem.get_default_system()
            if rpg_system:
                validated_data['rpg_system'] = rpg_system

        # Sempre aplica o template do sistema ao criar
        if rpg_system and rpg_system.base_sheet_data:
            validated_data['sheet_data'] = rpg_system.base_sheet_data

        character = super().create(validated_data)
        return character
    
    def to_representation(self, instance):
        """Retorna a representação completa do personagem criado"""
        rpg_system_data = None
        if instance.rpg_system:
            rpg_system_data = {
                "slug": instance.rpg_system.slug,
                "name": instance.rpg_system.name,
                "description": instance.rpg_system.description,
                "is_active": instance.rpg_system.is_active,
                "is_default": instance.rpg_system.is_default,
            }
        
        user_info = None
        if instance.user:
            user_info = {
                'id': instance.user.id,
                'username': instance.user.username,
                'email': instance.user.email
            }
        
        return {
            "id": instance.id,
            "player_name": instance.player_name,
            "rpg_system": rpg_system_data,
            "system_name": instance.rpg_system.name if instance.rpg_system else None,
            "xp_total": instance.xp_total,
            "description": instance.description,
            "avatar_url": instance.avatar_url,
            "sheet_data": instance.sheet_data,
            "is_active": instance.is_active,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "user_info": user_info,
        }