from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Session, SessionInvite, SessionCharacter, SessionNote
from .serializers import SessionSerializer, SessionDetailSerializer, NoteSerializer

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['-created_at']
    search_fields = ['title', 'content']

    def get_queryset(self):
        return SessionNote.objects.filter(
            session__members__user=self.request.user,
            user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Apagado com sucesso"}, status=200)


from .services import add_user_to_session


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
        obj = super().get_object()
        if self.action == 'retrieve':
            obj = Session.objects.prefetch_related(
                'members__user',
                'session_characters__character',
                'session_characters__user',
                'invites',
                    'maps',
                    'items'
            ).get(pk=obj.pk)
        return obj

    def perform_create(self, serializer):
        session = serializer.save(master=self.request.user)
        add_user_to_session(session, self.request.user, role="MASTER")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Apagado com sucesso"}, status=200)

    @action(detail=True, methods=["post"])
    def create_invite(self, request, pk=None):
        try:
            session = self.get_object()

            if session.master != request.user:
                return Response({"error": "Apenas o mestre pode criar convites"}, status=403)

            max_uses = request.data.get("max_uses")
            expires_at = request.data.get("expires_at")

            invite = SessionInvite.objects.create(
                session=session,
                max_uses=max_uses,
                expires_at=expires_at
            )

            from .serializers import SessionInviteDetailSerializer
            serializer = SessionInviteDetailSerializer(invite, context={'request': request})

            return Response(serializer.data, status=201)

        except Session.DoesNotExist:
            return Response({"error": "Sessão não encontrada"}, status=404)
        except Exception as e:
            return Response({"error": f"Erro ao criar convite: {str(e)}"}, status=500)


class JoinSessionByCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")

        if not code:
            return Response({"error": "Código de convite é obrigatório"}, status=400)

        try:
            invite = SessionInvite.objects.get(code=code)
        except SessionInvite.DoesNotExist:
            return Response({"error": "Código de convite inválido"}, status=404)

        if not invite.is_valid:
            return Response({"error": "Convite expirado ou limite de usos atingido"}, status=400)

        session = invite.session

        try:
            add_user_to_session(session, request.user)

            invite.uses_count += 1
            invite.save()

            return Response({
                "message": "Entrou na sessão com sucesso",
                "session_id": str(session.id),
                "session_name": session.name
            })

        except Exception as e:
            return Response({"error": f"Erro ao entrar na sessão: {str(e)}"}, status=500)


class SelectCharacterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        session_id = request.data.get("session_id") or request.data.get("session")
        character_id = request.data.get("character_id") or request.data.get("character")

        if not session_id:
            return Response({"error": "session_id ou session é obrigatório"}, status=400)

        if not character_id:
            return Response({"error": "character_id ou character é obrigatório"}, status=400)

        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({"error": "Sessão não encontrada"}, status=404)

        if not session.members.filter(user=request.user).exists():
            return Response({"error": "Você não é membro desta sessão"}, status=403)

        try:
            from characters.models import Character
            character = Character.objects.get(
                id=character_id,
                user=request.user
            )
        except Character.DoesNotExist:
            return Response({"error": "Personagem não encontrado ou não pertence a você"}, status=404)

        try:
            session_character, created = SessionCharacter.objects.update_or_create(
                session=session,
                user=request.user,
                defaults={"character": character}
            )

            return Response({
                "status": "personagem selecionado",
                "session_id": str(session.id),
                "character_id": str(character.id),
                "character_name": character.player_name,
                "action": "created" if created else "updated"
            })

        except Exception as e:
            return Response({"error": f"Erro interno: {str(e)}"}, status=500)