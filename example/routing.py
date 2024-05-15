# chat/routing.py

from django.urls import re_path, path

from .consumers import SingleChannelConsumer

'''
recommend using path whenever you can!
The reasons:
- path was introduced with the goal of making things simpler, which is clearly the direction the Django devs want to go. 
  So, when using path you are following this direction, thus minimizing the risk of having to adapt your codebase to new changes.
- While path is not just a result of an attempt of making things simpler, it actually really does make things simpler and more readable, 
  which is a good reason alone to why path should be preferred if both choices are an option.

re_path exists for reasons, so there are cases when using re_path might still be a better option. 
One scenario is clearly when require very customized converter and reach the limit of what is feasible with custom converters for 'path'. 
Yet another scenario to use re_path could be when upgrading a system with rather complex url-converters form a Django 1.x to a 2.x: 
Simply replacing the url with re_path commands can be much more time-efficient and thus be a desirable approach.

We call the as_asgi() classmethod when routing our consumers. 
This returns an ASGI wrapper application that will instantiate a new consumer instance for each connection or scope. 
This is similar to Django’s as_view(), which plays the same role for per-request instances of class-based views.

URLRouter - channels.routing.URLRouter: 
Any captured groups will be provided in scope as the key url_route, 
a dict with a kwargs key containing a dict of the named regex groups and an args key with a list of positional regex groups. 
Note that named and unnamed groups cannot be mixed: Positional groups are discarded as soon as a single named group is matched.
e.g. room_name = self.scope['url_route']['kwargs']['room_name']
'''
websocket_urlpatterns = [
    # this is using WebsocketConsumer. It may have blocking and compartibility issues.
    # where it might not be suitable for applications that require heavy I/O operations or long-running tasks, 
    # as it can't take full advantage of asynchronous I/O.
    # re_path(r'ws/chat_v2/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),

    # trying out AsyncWebsocketConsumer to address some WebsocketConsumer concerns
    # re_path(r'ws/chat_v2/(?P<room_name>\w+)/$', consumers_async.ChatConsumer.as_asgi()),
    path(f'ws/example/<room_name>/', SingleChannelConsumer.as_asgi()),
]