from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SessionViewSet, JoinSessionByCodeView, SelectCharacterView

router = DefaultRouter()
router.register(r"sessions", SessionViewSet, basename="sessions")

urlpatterns = [
    path("", include(router.urls)),
    path("join-by-code/", JoinSessionByCodeView.as_view()),
    path("select-character/", SelectCharacterView.as_view()),
]