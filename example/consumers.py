from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from example.models import ChannelClient

'''
By default the send(), group_send(), group_add() and other functions are async functions, meaning you have to await them. 
If you need to call them from synchronous code, you’ll need to use the handy asgiref.sync.async_to_sync wrapper:
'''
class SingleChannelConsumer(WebsocketConsumer):

    def connect(self):
        # Make a database row with our channel name
        ChannelClient.objects.create(channel_name=self.channel_name)

    def disconnect(self, close_code):
        # Note that in some rare cases (power loss, etc) disconnect may fail
        # to run; this naive example would leave zombie channel names around.
        ChannelClient.objects.filter(channel_name=self.channel_name).delete()

    def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        self.send(text_data=event["text"])

    # async def chat_message(self, event):
    #     '''
    #     Called when someone has messaged our chat.
    #     '''
    #     # Send a message down to the client
    #     await self.send_json(
    #         {
    #             "msg_type": settings.MSG_TYPE_MESSAGE,
    #             "room": event["room_id"],
    #             "username": event["username"],
    #             "message": event["message"],
    #         },
    #     )  

