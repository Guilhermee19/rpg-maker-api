from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Session, SessionInvite, SessionCharacter
from .serializers import SessionSerializer
from .services import generate_invite_code, add_user_to_session


class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Session.objects.filter(
            members__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        session = serializer.save(master=self.request.user)

        add_user_to_session(session, self.request.user, role="MASTER")

    @action(detail=True, methods=["post"])
    def create_invite(self, request, pk=None):
        session = self.get_object()

        if session.master != request.user:
            return Response({"error": "Apenas o mestre pode criar convites"}, status=403)

        invite = SessionInvite.objects.create(
            session=session,
            code=generate_invite_code()
        )

        return Response({"code": invite.code})


class JoinSessionByCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")

        try:
            invite = SessionInvite.objects.get(code=code)
        except SessionInvite.DoesNotExist:
            return Response({"error": "Código inválido"}, status=400)

        session = invite.session

        add_user_to_session(session, request.user)

        invite.uses_count += 1
        invite.save()

        return Response({"session_id": str(session.id)})


class SelectCharacterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        session_id = request.data.get("session_id")
        character_id = request.data.get("character_id")

        from characters.models import Character

        character = Character.objects.get(
            id=character_id,
            user=request.user
        )

        SessionCharacter.objects.update_or_create(
            session_id=session_id,
            user=request.user,
            defaults={"character": character}
        )

        return Response({"status": "personagem selecionado"})