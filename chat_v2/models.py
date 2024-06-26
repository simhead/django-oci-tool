# chat/models.py

from django.contrib.auth.models import User
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    # title of Room row
    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'

class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    command = models.CharField(max_length=256, default='blank')
    content = models.TextField()
    timetaken = models.FloatField(default=0.0, blank=True)  # Added timetaken field
    timestamp = models.DateTimeField(auto_now_add=True)

    # title of Message row
    def __str__(self):
        return f'{self.user.username}: {self.room.name}'