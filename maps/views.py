from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import SessionMap
from .serializers import SessionMapSerializer
from .permissions import IsSessionMember, IsSessionGM

class SessionMapViewSet(viewsets.ModelViewSet):
    serializer_class = SessionMapSerializer
    permission_classes = [permissions.IsAuthenticated, IsSessionMember]

    def get_queryset(self):
        # só mapas de sessões onde o user participa
        return SessionMap.objects.filter(session__members__user=self.request.user).distinct()

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
        if instance.session.gm != self.request.user:
            raise PermissionDenied("Apenas o mestre pode remover mapas.")
        instance.delete()