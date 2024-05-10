# chat/views.py

from django.shortcuts import render

from chat_v2.models import Room


def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    context = {
        'room': chat_room,
        'directory': './',
    }
    return render(request, 'room.html', context)

# def room_view(request, room_name):
#     return render(request, "room.html", {"room_name": room_name})