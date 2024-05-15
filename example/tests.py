from django.test import TestCase
from channels.testing import WebsocketCommunicator
from example.consumers import SingleChannelConsumer

'''
python -m pip install -U pytest-django pytest-asyncio

python manage.py test example.tests
'''
class SingleChannelConsumerTest(TestCase):
    """Tests for SingleChannelConsumer."""

    async def test_connect_and_disconnect(self):
        """Tests connection and disconnection behavior."""
        communicator = WebsocketCommunicator(SingleChannelConsumer.as_asgi(), "/ws/example/test")
        connected, subprotocol = await communicator.connect()
        assert connected
        # Test sending text
        await communicator.send_to(text_data="hello")
        response = await communicator.receive_from()
        assert response == "hello"
        # Close
        # await communicator.disconnect()

    # async def test_chat_message(self):
    #     """Tests handling of the 'chat.message' event."""
    #     async with HttpCommunicator(SingleChannelConsumer.as_asgi()) as comm:
    #         # Simulate websocket connection by opening a connection
    #         await comm.connect()

    #         # Send a chat message event
    #         message = {"type": "chat.message", "text": "Hi, message!"}
    #         await comm.send_json(message)

    #         # Receive the message back from the consumer
    #         response = await comm.receive_json()
    #         self.assertEqual(response["text"], "Hi, message!")

    #         # Simulate disconnection by closing the connection
    #         await comm.disconnect()
