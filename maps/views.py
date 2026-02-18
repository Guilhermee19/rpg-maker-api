from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import SessionMap
from .serializers import (
    SessionMapSerializer, 
    SessionMapCreateSerializer,
    SessionMapDetailSerializer
)
from .permissions import IsSessionMember, IsSessionGM
from session.models import Session

class SessionMapViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsSessionMember]
    
    def get_queryset(self):
        queryset = SessionMap.objects.filter(
            session__members__user=self.request.user
        ).select_related('session', 'session__master').distinct()
        
        # Filtro por sessão
        session_id = self.request.query_params.get('session')
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        
        # Filtro por status ativo
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            if is_active.lower() in ['true', '1']:
                queryset = queryset.filter(is_active=True)
            elif is_active.lower() in ['false', '0']:
                queryset = queryset.filter(is_active=False)
        
        # Busca por nome
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
            
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SessionMapCreateSerializer
        elif self.action == 'retrieve':
            return SessionMapDetailSerializer
        return SessionMapSerializer

    def perform_create(self, serializer):
        session = serializer.validated_data["session"]
        if session.master != self.request.user:
            raise PermissionDenied("Apenas o mestre pode criar mapas.")
        serializer.save()

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.session.master != self.request.user:
            raise PermissionDenied("Apenas o mestre pode editar mapas.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.session.master != self.request.user:
            raise PermissionDenied("Apenas o mestre pode remover mapas.")
        instance.delete()
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Ativa/desativa um mapa"""
        map_obj = self.get_object()
        if map_obj.session.master != request.user:
            raise PermissionDenied("Apenas o mestre pode ativar/desativar mapas.")
        
        map_obj.is_active = not map_obj.is_active
        map_obj.save()
        
        serializer = self.get_serializer(map_obj)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_session(self, request):
        """Lista mapas de uma sessão específica"""
        session_id = request.query_params.get('session_id')
        if not session_id:
            return Response(
                {'error': 'session_id é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response(
                {'error': 'Sessão não encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verifica se o usuário é membro da sessão
        if not session.members.filter(user=request.user).exists():
            raise PermissionDenied("Você não tem acesso a esta sessão.")
        
        maps = SessionMap.objects.filter(session=session).order_by('-created_at')
        serializer = self.get_serializer(maps, many=True)
        return Response(serializer.data)