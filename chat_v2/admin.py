# chat/admin.py

from django.contrib import admin

from chat_v2.models import Room, Message

admin.site.register(Room)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'command', 'get_timetaken', 'timestamp']  # Fields to display in the admin list
    search_fields = ['user__username', 'room__name', 'command']  # Allow searching by these fields

    def get_timetaken(self, obj):
        # Define a custom function to display 'timetaken' as 'TimeTaken (secs)'
        return f'{obj.timetaken}'

    get_timetaken.short_description = 'TimeTaken (secs)'  # Set the short description for the custom function

