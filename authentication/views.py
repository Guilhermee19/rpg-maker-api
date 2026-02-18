from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from .serializers import EmailTokenObtainPairSerializer, UserRegisterSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


@extend_schema(
    summary="Registrar novo usuário",
    description="Cria uma nova conta de usuário com email obrigatório",
    tags=["Autenticação"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Registrar novo usuário com email obrigatório"""
    """Registrar novo usuário com email obrigatório"""
    serializer = UserRegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        return Response({
            'message': 'Usuário criado com sucesso',
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'access': str(access_token),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Login do usuário",
    description="Autentica o usuário usando email e senha",
    tags=["Autenticação"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login do usuário com email"""
    serializer = EmailTokenObtainPairSerializer(data=request.data)
    
    if serializer.is_valid():
        return Response({
            'message': 'Login realizado com sucesso',
            **serializer.validated_data
        }, status=status.HTTP_200_OK)
    
    return Response(
        {'error': 'Email ou senha inválidos'}, 
        status=status.HTTP_401_UNAUTHORIZED
    )


@extend_schema(
    summary="Logout do usuário",
    description="Faz logout do usuário e invalida o refresh token",
    tags=["Autenticação"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout do usuário (blacklist do refresh token)"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': 'Logout realizado com sucesso'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Token inválido'
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Obter perfil do usuário",
    description="Retorna informações do usuário autenticado",
    tags=["Usuário"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    """Obter informações do usuário atual"""
    serializer = UserProfileSerializer(request.user)
    return Response({
        'user': serializer.data
    }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Renovar token de acesso",
    description="Renova o token de acesso usando o refresh token",
    tags=["Autenticação"]
)
class CustomTokenRefreshView(TokenRefreshView):
    """Custom refresh token view"""
    pass