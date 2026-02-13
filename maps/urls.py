from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SessionMapViewSet

router = DefaultRouter()
router.register(r"maps", SessionMapViewSet, basename="maps")

urlpatterns = [path("", include(router.urls))]