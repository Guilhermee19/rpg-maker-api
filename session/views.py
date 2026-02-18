from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Session, SessionInvite, SessionCharacter
from .serializers import SessionSerializer, SessionDetailSerializer
from .services import generate_invite_code, add_user_to_session

@extend_schema_view(
    list=extend_schema(
        summary="Listar sessões",
        description="Lista todas as sessões em que o usuário participa"
    ),
    create=extend_schema(
        summary="Criar sessão", 
        description="Cria uma nova sessão de RPG (usuário automaticamente se torna o mestre)"
    ),
    retrieve=extend_schema(
        summary="Detalhes da sessão",
        description="Obtém detalhes completos de uma sessão (membros, personagens, convites e mapas)"
    ),
    update=extend_schema(
        summary="Atualizar sessão",
        description="Atualiza completamente uma sessão (apenas o mestre)"
    ),
    partial_update=extend_schema(
        summary="Atualizar sessão parcialmente", 
        description="Atualiza parcialmente uma sessão (apenas o mestre)"
    ),
    destroy=extend_schema(
        summary="Deletar sessão",
        description="Remove uma sessão permanentemente (apenas o mestre)"
    )
)
class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Session.objects.filter(
            members__user=self.request.user
        ).distinct()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SessionDetailSerializer
        return SessionSerializer

    def get_object(self):
        """Override para fazer prefetch das relações no retrieve"""
        obj = super().get_object()
        if self.action == 'retrieve':
            # Fazendo prefetch de todas as relações para otimizar as queries
            obj = Session.objects.prefetch_related(
                'members__user',
                'session_characters__character',
                'session_characters__user', 
                'invites',
                'maps'
            ).get(pk=obj.pk)
        return obj

    def perform_create(self, serializer):
        session = serializer.save(master=self.request.user)

        add_user_to_session(session, self.request.user, role="MASTER")

    @extend_schema(
        summary="Criar convite",
        description="Cria um código de convite para a sessão (apenas o mestre)"
    )
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


@extend_schema(
    summary="Entrar na sessão por código",
    description="Permite que um usuário entre em uma sessão usando um código de convite"
)
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


@extend_schema(
    summary="Selecionar personagem para sessão",
    description="Define qual personagem o usuário irá usar na sessão"
)
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