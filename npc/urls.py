from rest_framework import routers
from .views import NPCViewSet

router = routers.DefaultRouter()
router.register(r'npcs', NPCViewSet, basename='npc')

urlpatterns = router.urls
