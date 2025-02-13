
from django.urls import re_path

from . import notify

websocket_urlpatterns = [
    re_path(r"ws/message/(?P<group_name>[\w+|\-?]+)+/(?P<username>\w+)$", notify.MessageNotify.as_asgi()),
]
