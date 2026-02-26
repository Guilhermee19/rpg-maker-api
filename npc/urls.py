
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NPCViewSet

router = DefaultRouter()
router.register(r'npcs', NPCViewSet, basename='npc')

urlpatterns = [
	path('', include(router.urls)),
]
