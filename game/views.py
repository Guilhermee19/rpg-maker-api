from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import CharacterClass, Character, Item, CharacterItem, Skill, CharacterSkill
from .serializers import (
    CharacterClassSerializer, CharacterSerializer, CharacterCreateSerializer,
    ItemSerializer, CharacterItemSerializer, SkillSerializer, CharacterSkillSerializer
)


class CharacterClassViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for character classes (read-only)"""
    queryset = CharacterClass.objects.all()
    serializer_class = CharacterClassSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'base_health', 'base_attack']
    ordering = ['name']


class CharacterViewSet(viewsets.ModelViewSet):
    """ViewSet for player characters"""
    serializer_class = CharacterSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['character_class', 'level']
    search_fields = ['name']
    ordering_fields = ['name', 'level', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return only characters owned by the current user"""
        return Character.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        """Use simplified serializer for creation"""
        if self.action == 'create':
            return CharacterCreateSerializer
        return CharacterSerializer
    
    def perform_create(self, serializer):
        """Set the owner to the current user and initialize stats"""
        character = serializer.save(owner=self.request.user)
        character.current_health = character.max_health
        character.current_mana = character.max_mana
        character.save()
    
    @action(detail=True, methods=['post'])
    def heal(self, request, pk=None):
        """Heal character to full health"""
        character = self.get_object()
        character.current_health = character.max_health
        character.current_mana = character.max_mana
        character.save()
        
        serializer = CharacterSerializer(character)
        return Response({
            'message': f'{character.name} has been fully healed!',
            'character': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def level_up(self, request, pk=None):
        """Level up character (for testing purposes)"""
        character = self.get_object()
        character.level += 1
        character.experience = 0  # Reset experience after level up
        character.current_health = character.max_health
        character.current_mana = character.max_mana
        character.save()
        
        serializer = CharacterSerializer(character)
        return Response({
            'message': f'{character.name} leveled up to level {character.level}!',
            'character': serializer.data
        })


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for items (read-only for now)"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['item_type', 'rarity']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'value', 'rarity']
    ordering = ['name']


class CharacterItemViewSet(viewsets.ModelViewSet):
    """ViewSet for character inventory"""
    serializer_class = CharacterItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_equipped', 'item__item_type']
    search_fields = ['item__name']
    ordering = ['item__name']
    
    def get_queryset(self):
        """Return only inventory items for characters owned by current user"""
        return CharacterItem.objects.filter(character__owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def equip(self, request, pk=None):
        """Equip/unequip an item"""
        character_item = self.get_object()
        character_item.is_equipped = not character_item.is_equipped
        character_item.save()
        
        status_text = 'equipped' if character_item.is_equipped else 'unequipped'
        return Response({
            'message': f'{character_item.item.name} has been {status_text}',
            'is_equipped': character_item.is_equipped
        })


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for skills (read-only for now)"""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['required_level', 'character_classes']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'required_level', 'mana_cost']
    ordering = ['required_level', 'name']


class CharacterSkillViewSet(viewsets.ModelViewSet):
    """ViewSet for character skills"""
    serializer_class = CharacterSkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['skill_level']
    search_fields = ['skill__name']
    ordering = ['skill__name']
    
    def get_queryset(self):
        """Return only skills for characters owned by current user"""
        return CharacterSkill.objects.filter(character__owner=self.request.user)