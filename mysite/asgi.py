"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels_redis.core import RedisChannelLayer
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import chat.routing
import chat_v2.routing
from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from chat_v2.routing import websocket_urlpatterns as chat_v2_websocket_urlpatterns
from chat_v2.consumers_async import GenerateConsumer, DeleteConsumer

# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(URLRouter(chat_v2.routing.websocket_urlpatterns))
#         ),
#     }
# )

'''
To open another WebSocket for chat.routing, 
modify application variable to include another WebSocket route for the chat.routing.websocket_urlpatterns. 

Adding another chat room/workspace with chat_v2 with associated Consumer defined in chat_v2.routing

URLs and Consumer are all defined in routing.py
'''
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    chat_websocket_urlpatterns + chat_v2_websocket_urlpatterns
                )
            )
        ),
        # "channel": RedisChannelLayer(),
        "channel": ChannelNameRouter({
            "thumbnails-generate": GenerateConsumer.as_asgi(),
            "thumbnails-delete": DeleteConsumer.as_asgi(),
        }),
    }
)