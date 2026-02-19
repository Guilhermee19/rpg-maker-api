from rest_framework import permissions
from session.models import SessionMember

class IsSessionMember(permissions.BasePermission):
    """
    Permission para verificar se o usuário é membro da sessão.
    Para criação: deixa o serializer validar (mais específico)
    Para objetos: verifica se o usuário é membro da sessão do objeto
    """
    
    def has_permission(self, request, view):
        # Para actions que não precisam de um objeto específico
        if view.action in ['list', 'by_session']:
            return True
        
        # Para criação, deixa o serializer validar (mais detalhado)
        if view.action == 'create':
            return True
        
        # Para outras actions, será verificado no has_object_permission
        return True

    def has_object_permission(self, request, view, obj):
        """Verifica se o usuário é membro da sessão ou master"""
        is_master = obj.session.master == request.user
        is_member = obj.session.members.filter(user=request.user).exists()
        return is_master or is_member


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