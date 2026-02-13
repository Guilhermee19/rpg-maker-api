from rest_framework import viewsets, permissions
from .models import Character
from .serializers import CharacterSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id

class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Usuário só vê os próprios personagens
        return Character.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Usuário sempre vem do token, não do payload
        serializer.save(user=self.request.user)