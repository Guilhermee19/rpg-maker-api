from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SessionViewSet, JoinSessionByCodeView, SelectCharacterView, NoteViewSet, PlayerSessionsListView, MasterSessionsListView


router = DefaultRouter()
router.register(r"sessions", SessionViewSet, basename="sessions")
router.register(r"notes", NoteViewSet, basename="notes")

urlpatterns = [
    path("", include(router.urls)),
    path("join-by-code/", JoinSessionByCodeView.as_view()),
    path("select-character/", SelectCharacterView.as_view()),
    path("player-sessions/", PlayerSessionsListView.as_view(), name="player-sessions"),
    path("master-sessions/", MasterSessionsListView.as_view(), name="master-sessions"),
]