from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet
from characters.views import CharacterViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename="users")
router.register(r'profiles', ProfileViewSet, basename="profiles")
router.register(r"characters", CharacterViewSet, basename="characters")


urlpatterns = [
    path('', include(router.urls)),
]