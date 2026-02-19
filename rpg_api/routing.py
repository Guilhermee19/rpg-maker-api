from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # O código da sala vai na URL: ws/session/SALA123/
    re_path(r'ws/session/(?P<room_code>\w+)/$', consumers.DiceConsumer.as_asgi()),
]