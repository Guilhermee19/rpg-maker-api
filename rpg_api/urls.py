from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny  
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """Root API endpoint com informações sobre rotas disponíveis"""
    return Response({
        'message': 'RPG Maker API',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'get_user': '/api/v1/auth/get-user/',
                'login': '/api/v1/auth/login/',
                'register': '/api/v1/auth/register/',
                'logout': '/api/v1/auth/logout/',
                'refresh_token': '/api/v1/auth/token/refresh/'
            },
            'characters': {
                'characters': '/api/v1/core/characters/'
            },
            'session': {
                'sessions': '/api/v1/session/sessions/',
                'invites': '/api/v1/session/invites/',
                'members': '/api/v1/session/members/',
                'session_characters': '/api/v1/session/session-characters/'
            },
            'documentation': {
                'swagger': '/api/docs/',
                'redoc': '/api/redoc/',
                'schema': '/api/schema/'
            }
        }
    })

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Root
    path('api/', api_root, name='api-root'),
    path('api/v1/', api_root, name='api-v1-root'),
    
    # API Documentation  
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    path('api/v1/auth/', include('authentication.urls')),  # Login, Register, Logout
    path('api/v1/core/', include('core.urls')),           # Users, Characters (ViewSets)  
    path('api/v1/session/', include('session.urls')),     # Sessions, Invites (ViewSets)
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)