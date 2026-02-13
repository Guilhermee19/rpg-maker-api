from rest_framework import permissions
from session.models import SessionMember

class IsSessionMember(permissions.BasePermission):
    def has_permission(self, request, view):
        session_id = request.data.get("session") or request.query_params.get("session")
        if not session_id and view.kwargs.get("pk"):
            return True  # object-level depois
        if not session_id:
            return False
        return SessionMember.objects.filter(session_id=session_id, user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        return obj.session.members.filter(user=request.user).exists()


class IsSessionGM(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.session.master == request.user