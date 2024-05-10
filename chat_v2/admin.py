# chat/admin.py

from django.contrib import admin

from chat_v2.models import Room, Message

admin.site.register(Room)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'timestamp']  # Fields to display in the admin list
    search_fields = ['user__username', 'room__name']  # Allow searching by these fields
