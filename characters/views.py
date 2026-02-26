from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from asgiref.sync import sync_to_async
from .models import Character, RPGSystem
from .serializers import (
    CharacterSerializer, 
    CharacterCreateSerializer,
    RPGSystemSerializer, 
    RPGSystemListSerializer
)


class IsOwner(permissions.BasePermission):
    """Permission para garantir que usuários só acessem seus próprios personagens"""
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class RPGSystemViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para consulta de sistemas de RPG"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas sistemas ativos"""
        return RPGSystem.objects.filter(is_active=True).order_by('name')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RPGSystemListSerializer
        return RPGSystemSerializer
    
    @action(detail=False, methods=['get'])
    def default(self, request):
        """Retorna o sistema padrão"""
        default_system = RPGSystem.get_default_system()
        if default_system:
            serializer = self.get_serializer(default_system)
            return Response(serializer.data)
        return Response(
            {'error': 'Nenhum sistema padrão configurado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    @action(detail=True, methods=['get'])
    def template(self, request, pk=None):
        """Retorna o template base da ficha para o sistema"""
        system = self.get_object()
        return Response({
            'system': system.name,
            'base_sheet_data': system.base_sheet_data
        })


class CharacterViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento completo de personagens"""
    
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Retorna apenas personagens do usuário autenticado"""
        return Character.objects.filter(user=self.request.user).select_related('rpg_system').order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CharacterCreateSerializer
        return CharacterSerializer

    def perform_create(self, serializer):
        """Associa o personagem ao usuário autenticado"""
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Apagado com sucesso"}, status=200)

    @action(detail=True, methods=['post'])
    def reset_sheet(self, request, pk=None):
        """Reseta a ficha do personagem para o template do sistema"""
        character = self.get_object()
        
        if character.rpg_system and character.rpg_system.base_sheet_data:
            character.sheet_data = character.rpg_system.base_sheet_data
            character.save()
            
            serializer = self.get_serializer(character)
            return Response({
                'success': True,
                'message': f'Ficha resetada para o template do sistema {character.rpg_system.name}',
                'character': serializer.data
            })
        
        return Response(
            {'error': 'Personagem não possui sistema definido ou sistema sem template'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def change_system(self, request, pk=None):
        """Troca o sistema de RPG do personagem"""
        character = self.get_object()
        system_id = request.data.get('rpg_system_id')
        apply_template = request.data.get('apply_template', False)
        
        try:
            new_system = RPGSystem.objects.get(id=system_id, is_active=True)
        except RPGSystem.DoesNotExist:
            return Response(
                {'error': 'Sistema de RPG não encontrado ou não ativo'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        character.rpg_system = new_system
        
        # Aplica o template se solicitado
        if apply_template and new_system.base_sheet_data:
            character.sheet_data = new_system.base_sheet_data
        
        character.save()
        
        serializer = self.get_serializer(character)
        return Response({
            'success': True,
            'message': f'Sistema alterado para {new_system.name}',
            'template_applied': apply_template,
            'character': serializer.data
        })