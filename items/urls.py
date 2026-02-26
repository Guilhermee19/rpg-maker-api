from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ItemViewSet

router = SimpleRouter()
router.register(r'items', ItemViewSet, basename='items')

urlpatterns = [
    path('', include(router.urls)),
]