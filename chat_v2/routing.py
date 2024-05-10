# chat/routing.py

from django.urls import re_path

from . import consumers, consumers_async

websocket_urlpatterns = [
    # this is using WebsocketConsumer. It may have blocking and compartibility issues.
    # where it might not be suitable for applications that require heavy I/O operations or long-running tasks, 
    # as it can't take full advantage of asynchronous I/O.
    re_path(r'ws/chat_v2/(?P<room_name>\w+)/$', consumers_async.ChatConsumer.as_asgi()),

    # trying out AsyncWebsocketConsumer to address some WebsocketConsumer concerns
    #re_path(r'ws/chat_v2_async/(?P<room_name>\w+)/$', consumers_async.ChatConsumer.as_asgi()),
]