from django.db import models

class ChannelClient(models.Model):
    channel_name = models.CharField(max_length=255, unique=True)
    '''
    The user field is a foreign key to the User model from Django's auth app (optional, for user association). 
    Set null=True and blank=True to allow anonymous connections.
    '''
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    session_id = models.CharField(max_length=255, null=True, blank=True)  # Optional for session tracking
    connected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'channel_clients'  # Optional custom table name

    def __str__(self):
        return f"Client: {self.channel_name} (user: {self.user})"

