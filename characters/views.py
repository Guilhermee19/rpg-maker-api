from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Character
from .serializers import CharacterSerializer

class IsOwner(permissions.BasePermission):
    """Permission para garantir que usuários só acessem seus próprios personagens"""
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


@extend_schema_view(
    list=extend_schema(
        summary="Lista personagens do usuário",
        description="Retorna todos os personagens do usuário autenticado"
    ),
    create=extend_schema(
        summary="Criar novo personagem", 
        description="Cria um novo personagem para o usuário autenticado"
    ),
    retrieve=extend_schema(
        summary="Detalhes do personagem",
        description="Retorna detalhes de um personagem específico"
    ),
    update=extend_schema(
        summary="Atualizar personagem",
        description="Atualiza completamente um personagem"
    ),
    partial_update=extend_schema(
        summary="Atualizar personagem parcialmente", 
        description="Atualiza campos específicos de um personagem"
    ),
    destroy=extend_schema(
        summary="Excluir personagem",
        description="Remove um personagem permanentemente"
    ),
)
class CharacterViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento completo de personagens"""
    
    serializer_class = CharacterSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Retorna apenas personagens do usuário autenticado"""
        return Character.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """Associa o personagem ao usuário autenticado"""
        serializer.save(user=self.request.user)