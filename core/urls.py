from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from characters.views import CharacterViewSet, RPGSystemViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename="users")
router.register(r"characters", CharacterViewSet, basename="characters")
router.register(r"rpg-systems", RPGSystemViewSet, basename="rpg-systems")

urlpatterns = [
    path('', include(router.urls)),
]