from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.models import User
from rest_framework import serializers
from .serializers import EmailTokenObtainPairSerializer, UserRegisterSerializer
from django.core.mail import send_mail
from django.conf import settings
from .models import PasswordResetToken
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    """Obter informações do usuário atual"""
    serializer = UserProfileSerializer(request.user)
    return Response({
        'user': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """
    Envia email com link de redefinição de senha.
    Sempre retorna 200 para não revelar se o email existe.
    """
    serializer = ForgotPasswordSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']

    try:
        user = User.objects.get(email__iexact=email)
        reset_token = PasswordResetToken.generate_token(user)

        reset_url = (
            f"{settings.FRONTEND_URL}/reset-password"
            f"?email={email}"
            f"&token={reset_token.token}"
        )

        send_mail(
            subject='Redefinição de senha',
            message=(
                f'Olá, {user.first_name or user.username}!\n\n'
                f'Recebemos uma solicitação para redefinir sua senha.\n'
                f'Clique no link abaixo para criar uma nova senha:\n\n'
                f'{reset_url}\n\n'
                f'Este link expira em {PasswordResetToken.EXPIRY_HOURS} horas.\n'
                f'Se você não solicitou isso, ignore este email.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        pass
    except Exception as e:
        # Loga o erro real sem retornar 500
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Erro ao enviar email de reset: {str(e)}')
        return Response(
            {'error': f'Erro ao enviar email: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(
        {'message': 'Se este email estiver cadastrado, você receberá as instruções em breve.'},
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """
    Redefine a senha usando email + token hash recebidos no link.
    """
    serializer = ResetPasswordSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']
    token_value = serializer.validated_data['token']
    new_password = serializer.validated_data['new_password']

    try:
        user = User.objects.get(email__iexact=email)
        reset_token = PasswordResetToken.objects.get(token=token_value, user=user)
    except (User.DoesNotExist, PasswordResetToken.DoesNotExist):
        return Response(
            {'error': 'Token inválido ou expirado.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not reset_token.is_valid():
        return Response(
            {'error': 'Token inválido ou expirado.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Atualiza a senha e invalida o token
    user.set_password(new_password)
    user.save()

    reset_token.used = True
    reset_token.save()

    return Response(
        {'message': 'Senha redefinida com sucesso.'},
        status=status.HTTP_200_OK,
    )

class CustomTokenRefreshView(TokenRefreshView):
    """Custom refresh token view"""
    pass