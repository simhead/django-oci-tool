# chat/consumers.py

import json
import subprocess, time

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Room, Message
from django.contrib.auth.models import User  # Import User model

allowed_commands = ['ls', 'ls -al', 'ls -l', 'terraform']  # Example whitelist

def executeCommand(command, directory):
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

        # Join workspace group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # connection has to be accepted
        await self.accept()

    async def disconnect(self, close_code):
        # Leave workspace group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    async def receive(self, text_data=None, bytes_data=None):
        # Capture start time before processing the message
        start_time = time.perf_counter()  # Use high-resolution timer

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        channel = text_data_json['channel']
        # Extract command from data
        command = text_data_json['command']
        directory = text_data_json['directory']
        
        print(f'Check received data: {text_data_json}')

        # Check if command is allowed (e.g., whitelist specific commands)
        # allowed_commands = ['ls', 'ls -al', 'ls -l']  # Example whitelist
        # if command not in allowed_commands:
        #     # Handle unauthorized command
        #     return
        
        # execute command
        command_results = executeCommand(command, directory)
        print(f'Results: \n[\n{command_results}]') 
        # # Get Room instance based on channel name
        # try:
        #     room = Room.objects.get(name=channel)
        # except Room.DoesNotExist:
        #     # Handle case where room does not exist
        #     # You can either ignore the message or handle it accordingly
        #     return
        
        # # Get User instance based on username
        # try:
        #     user = User.objects.get(username='admin')
        # except User.DoesNotExist:
        #     # Handle case where user does not exist
        #     # You can either ignore the message or handle it accordingly
        #     return

        # # Save to database
        # Message.objects.create(room=room, user=user, content=message)
        
        # Calculate elapsed time for processing
        processing_time = time.perf_counter() - start_time

        print(f'Processing Time: {processing_time:.4f} seconds')

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


    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))