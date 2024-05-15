# chat/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from chat_v2.models import Room

# add the @login_required decorator from Django's django.contrib.auth.decorators module to your views to restrict access only to authenticated users:

# @login_required
def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })


# @login_required
def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    context = {
        'room': chat_room,
        'directory': './',
    }
    return render(request, 'room.html', context)

# def room_view(request, room_name):
#     return render(request, "room.html", {"room_name": room_name})