from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CharacterClassViewSet, CharacterViewSet, ItemViewSet, 
    CharacterItemViewSet, SkillViewSet, CharacterSkillViewSet
)

router = DefaultRouter()
router.register(r'character-classes', CharacterClassViewSet)
router.register(r'characters', CharacterViewSet, basename='character')
router.register(r'items', ItemViewSet)
router.register(r'inventory', CharacterItemViewSet, basename='characteritem')
router.register(r'skills', SkillViewSet)
router.register(r'character-skills', CharacterSkillViewSet, basename='characterskill')

urlpatterns = [
    path('', include(router.urls)),
]