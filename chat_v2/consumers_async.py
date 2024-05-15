# chat/consumers.py
'''
When a user posts a message, a JavaScript function will transmit the message over WebSocket to a ChatConsumer. 
The ChatConsumer will receive that message and forward it to the group corresponding to the room/workspace name. 
Every ChatConsumer in the same group (and thus in the same room) will then receive the message from the group and 
forward it over WebSocket back to JavaScript, where it will be appended to the chat log.

Channels ships with generic consumers that wrap common functionality up so you don’t need to rewrite it, specifically for HTTP and WebSocket handling.
https://channels.readthedocs.io/en/latest/topics/consumers.html
'''
import json
import subprocess, time

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login

from .models import Room, Message
from django.contrib.auth.models import User  # Import User model

allowed_commands = ['ls', 'ls -al', 'ls -l', 'terraform']  # Example whitelist

def executeCommand(command, directory):
    # Check if command is allowed (e.g., whitelist specific commands)
        # allowed_commands = ['ls', 'ls -al', 'ls -l']  # Example whitelist
        # if command not in allowed_commands:
        #     # Handle unauthorized command
        #     return
        
    # Execute command securely
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=directory,
        )
        output, error = process.communicate()
        if error:
            # Handle command execution error
            print(f'Failed to run: {command} - {error}')
            return
    except Exception as e:
        # Handle command execution exception
        print(f'Exception for {command} - {e}')
        return
    
    # Decode the output bytes to a string using UTF-8 encoding
    output_str = output.decode('utf-8')
    return output_str
        
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        subprotocols = self.scope['subprotocols']
        self.user = self.scope["user"]
        self.session = self.scope["session"]

        # print(f'Client requested for connection: {self.room_group_name}-{self.room_name}-{subprotocols}:{self.user}-{self.session}')

        # Join workspace group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # connection has to be accepted
        await self.accept()

    async def disconnect(self, close_code):
        # Leave workspace group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def publish_message_to_redis(self, message, channel, command_results, processing_time):
        try:
            # Publish message to Redis channel
            self.channel_layer.send(
                "thumbnails-generate",
                {
                    # Note that the event you send must have a type key, even if only one type of message is being sent over the channel, 
                    # as it will turn into an event a consumer has to handle.
                    "type": "generate",
                    "id": 123456789,
                },
            )

            print(f'Message published to Redis channel {channel}')  # Print success message
        except Exception as e:
            print(f'Error publishing message to Redis: {e}')  # Print error message with exception details


    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        print(f'From Workspace websocket - received: {self.room_group_name}-{self.room_name}:{self.user}-{self.session}')
        # Capture start time before processing the message
        start_time = time.perf_counter()  # Use high-resolution timer

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        channel = text_data_json['channel']
        # Extract command from data
        command = text_data_json['command']
        directory = text_data_json['directory']
        
        print(f'Check received data: {text_data_json}')

        # Retrieve the Room instance based on the channel name
        try:
            # Use sync_to_async to make the ORM query asynchronous-compatible
            room = await sync_to_async(Room.objects.get)(name=channel)
            print("Room object name:", room.name)
        except Room.DoesNotExist:
            # Handle the case where the room does not exist
            print(f"Room with name '{channel}' does not exist.")
            return
        
        # execute command
        command_results = executeCommand(command, directory)
        # print(f'Results: \n[\n{command_results}]') 
        
        # Get User instance based on username
        try:
            user = await sync_to_async(User.objects.get)(username='admin')
            print(f"Username object found: {user.first_name}")
        except User.DoesNotExist:
            # Handle case where user does not exist
            # You can either ignore the message or handle it accordingly
            print(f"username: 'admin' does not exist.")
            return

        # Calculate elapsed time for processing
        processing_time = time.perf_counter() - start_time
         # Round processing time to 4 decimal places
        processing_time = round(processing_time, 4)

        # Publish message to Redis Pub/Sub
        # await self.publish_message_to_redis(message, channel, command_results, processing_time)

        print(f'Processing Time: {processing_time:.4f} seconds')
        time_taken = f'Processing Time: {processing_time:.4f} seconds'
        line_contents = '> '+command+'\n'+command_results+'\n'+time_taken
        # Save to database
        await sync_to_async(Message.objects.create)(room=room, user=user, command=command, timetaken=processing_time, content=line_contents)
        
        try:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'results': command_results,
                    'processing_time': processing_time,
                }
            )
            print(f'Response Message sent successfully.')  # Assuming successful send within try block
        except Exception as e:
            print(f'Error sending response message: {e}')  # Print any exceptions encountered

    # Receive message from room group
    # async def chat_message(self, event):
    #     message = event["message"]

    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({"message": message}))

    # Receive message from room group
    # handler for message type chat_message
    async def chat_message(self, event):
        print(f'From Workspace group and return back to javascript client')
        await self.send(text_data=json.dumps(event))


class GenerateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get details about the connection (optional)
        print(f"GenerateConsumer connected: {self.scope}")
        await self.channel_layer.group_add("thumbnails_generation", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Clean up resources or group membership (optional)
        print(f"GenerateConsumer disconnected: {close_code}")
        await self.channel_layer.group_discard("thumbnails_generation", self.channel_name)

    async def receive(self, text_data):
        # Handle incoming messages related to thumbnail generation
        data = json.loads(text_data)  # Assuming JSON data
        print(f"Received data for thumbnail generation: {data}")
        
        # Logic to process the data and generate thumbnails
        # This might involve accessing files or external services

        # Send a response message (optional)
        await self.send(text_data=json.dumps({"message": "Thumbnails generated successfully!"}))

class DeleteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get details about the connection (optional)
        print(f"DeleteConsumer connected: {self.scope}")
        await self.accept()

    async def disconnect(self, close_code):
        # Clean up resources (optional)
        print(f"DeleteConsumer disconnected: {close_code}")

    async def receive(self, text_data):
        # Handle incoming messages related to thumbnail deletion
        data = json.loads(text_data)  # Assuming JSON data
        print(f"Received data for thumbnail deletion: {data}")
        
        # Logic to process the data and delete thumbnails
        # This might involve accessing and deleting files

        # Send a response message (optional)
        await self.send(text_data=json.dumps({"message": "Thumbnails deleted successfully!"}))