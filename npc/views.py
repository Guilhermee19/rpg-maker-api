
from rest_framework import viewsets, permissions, filters
from .models import NPC
from .serializers import NPCSerializer

class IsSessionMaster(permissions.BasePermission):
	"""
	Permite acesso apenas ao mestre da sessão para criar/editar/remover NPCs.
	"""
	def has_object_permission(self, request, view, obj):
		return obj.session.master == request.user

class NPCViewSet(viewsets.ModelViewSet):
	serializer_class = NPCSerializer
	permission_classes = [permissions.IsAuthenticated, IsSessionMaster]
	filter_backends = [filters.OrderingFilter, filters.SearchFilter]
	ordering = ['-created_at']
	search_fields = ['name', 'note']

	def get_queryset(self):
		# Mestre vê todos os NPCs das sessões que ele é mestre
		return NPC.objects.filter(session__master=self.request.user)

	def perform_create(self, serializer):
		# O usuário logado é sempre o criador (mestre)
		serializer.save(user=self.request.user)
