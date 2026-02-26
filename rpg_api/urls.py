from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Prevent duplicate registration of DRF's format suffix converter when multiple
# routers are constructed across apps. Wrap Django's register_converter to
# ignore ValueError raised on duplicate registrations.
from django.urls import converters as _converters
_orig_register = _converters.register_converter
def _safe_register(converter, name):
    try:
        return _orig_register(converter, name)
    except ValueError:
        return None
_converters.register_converter = _safe_register
 
# Also patch DRF's local reference to register_converter (it imports the
# function at module import time) so format_suffix_patterns calls won't
# raise when invoked multiple times.
try:
    import rest_framework.urlpatterns as _drf_urlpatterns
    _drf_orig = getattr(_drf_urlpatterns, 'register_converter', None)
    if _drf_orig is not None:
        def _drf_safe(converter, name):
            try:
                return _drf_orig(converter, name)
            except ValueError:
                return None
        _drf_urlpatterns.register_converter = _drf_safe
except Exception:
    pass
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation  
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    path('api/v1/auth/', include('authentication.urls')),  # Login, Register, Logout
    path('api/v1/core/', include('core.urls')),           # Users, Characters (ViewSets)  
    path('api/v1/session/', include('session.urls')),     # Sessions, Invites (ViewSets)
    path('api/v1/maps/', include('maps.urls')),           # Maps, Layers, Objects, Tokens
    path('api/v1/npc/', include('npc.urls')),            # NPCs
    path('api/v1/items/', include('items.urls')),        # Itens
]

# Static and Media files - Para desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)