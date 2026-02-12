from rest_framework import serializers
from .models import CharacterClass, Character, Item, CharacterItem, Skill, CharacterSkill


class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterClass
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ItemSerializer(serializers.ModelSerializer):
    rarity_display = serializers.CharField(source='get_rarity_display', read_only=True)
    item_type_display = serializers.CharField(source='get_item_type_display', read_only=True)
    
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CharacterItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), 
        source='item', 
        write_only=True
    )
    
    class Meta:
        model = CharacterItem
        fields = ['id', 'item', 'item_id', 'quantity', 'is_equipped', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class SkillSerializer(serializers.ModelSerializer):
    character_classes = CharacterClassSerializer(many=True, read_only=True)
    
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CharacterSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), 
        source='skill', 
        write_only=True
    )
    
    class Meta:
        model = CharacterSkill
        fields = ['id', 'skill', 'skill_id', 'skill_level', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CharacterSerializer(serializers.ModelSerializer):
    character_class_detail = CharacterClassSerializer(source='character_class', read_only=True)
    inventory = CharacterItemSerializer(many=True, read_only=True)
    skills = CharacterSkillSerializer(many=True, read_only=True)
    
    # Calculated stats (read-only)
    max_health = serializers.ReadOnlyField()
    max_mana = serializers.ReadOnlyField()
    attack = serializers.ReadOnlyField()
    defense = serializers.ReadOnlyField()
    speed = serializers.ReadOnlyField()
    
    class Meta:
        model = Character
        fields = [
            'id', 'name', 'character_class', 'character_class_detail', 
            'level', 'experience', 'current_health', 'current_mana',
            'max_health', 'max_mana', 'attack', 'defense', 'speed',
            'inventory', 'skills', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CharacterCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for character creation"""
    class Meta:
        model = Character
        fields = ['name', 'character_class']