from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializers import UserSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Perfil do usuário",
        description="Retorna informações do usuário autenticado"
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de perfil do usuário"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas o usuário autenticado"""
        return User.objects.filter(id=self.request.user.id)
    
    @extend_schema(
        summary="Perfil do usuário atual",
        description="Obtém ou atualiza informações do usuário autenticado"
    )
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Endpoint para gerenciar perfil do usuário atual"""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(
                request.user, 
                data=request.data, 
                partial=(request.method == 'PATCH')
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)