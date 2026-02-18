from rest_framework import permissions
from session.models import SessionMember

class IsSessionMember(permissions.BasePermission):
    """
    Permission para verificar se o usuário é membro da sessão.
    Para criação: verifica se o session_id nos dados da request está acessível
    Para objetos: verifica se o usuário é membro da sessão do objeto
    """
    
    def has_permission(self, request, view):
        # Para actions que não precisam de um objeto específico
        if view.action in ['list', 'by_session']:
            return True
        
        # Para criação, verifica se o usuário pode acessar a sessão informada
        if view.action == 'create':
            session_id = request.data.get("session")
            if not session_id:
                return False
            return SessionMember.objects.filter(
                session_id=session_id, 
                user=request.user
            ).exists()
        
        # Para outras actions, será verificado no has_object_permission
        return True

    def has_object_permission(self, request, view, obj):
        """Verifica se o usuário é membro da sessão do mapa"""
        return obj.session.members.filter(user=request.user).exists()


class IsSessionGM(permissions.BasePermission):
    """
    Permission para verificar se o usuário é o mestre (GM/Master) da sessão.
    """
    
    def has_permission(self, request, view):
        if view.action == 'create':
            session_id = request.data.get("session")
            if not session_id:
                return False
            try:
                from session.models import Session
                session = Session.objects.get(id=session_id)
                return session.master == request.user
            except Session.DoesNotExist:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        """Verifica se o usuário é o mestre da sessão"""
        return obj.session.master == request.user