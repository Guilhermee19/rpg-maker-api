from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from characters.views import CharacterViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename="users")
router.register(r"characters", CharacterViewSet, basename="characters")
# Rota profiles removida - usando users para gerenciar perfis


urlpatterns = [
    path('', include(router.urls)),
]