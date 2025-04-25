import websockets
from websockets.asyncio.client import connect
import json

class Moonraker:
    # Moonraker class to handle the connection to the Moonraker API
    # This class is responsible for sending and receiving messages

    def __init__(self, moonraker_url: str):
        self.moonraker_url = moonraker_url
        self.connected = False
        self.ws = None

    async def connect(self):
        # Connect to the Moonraker API
        # This method should establish a WebSocket connection to the Moonraker API
        try:
            self.ws = await connect(self.moonraker_url)
            self.connected = True
            print(f"Connected to Moonraker at {self.moonraker_url}")
        except Exception as e:
            print(f"Failed to connect to Moonraker: {e}")
            self.connected = False

    async def listen(self):
        # Listen for messages from the Moonraker API
        # This method should handle incoming messages from the Moonraker API
        if not self.connected or not self.ws:
            print("Not connected to Moonraker")
            return

        try:
            async for message in self.ws:
                print(f"Received message: {message}")
                # Process the message here
                # await self.process_message(message)
        except Exception as e:
            print(f"Error while listening to Moonraker: {e}")
            self.connected = False

    async def check_state(self):
        # JSON RPC request to the websocket server
        # jsonrpc: "2.0"
        # method: "server.info"
        # "id": 9546

        request_data = {
            "jsonrpc": "2.0",
            "method": "server.info",
            "id": 9546
        }
        if not self.connected or not self.ws:
            print("Not connected to Moonraker")
            return

        try:
            await self.ws.send(json.dumps(request_data))
            print("Sent request to Moonraker")
            response = await self.ws.recv()
            print(f"Received response: {response}")

        except Exception as e:
            print(f"Error while sending request to Moonraker: {e}")
            self.connected = False
