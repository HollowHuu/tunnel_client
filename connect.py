import asyncio
import websockets
import aiohttp
import json

RELAY_URL = "ws://localhost:9001"


class ServerConnection:
    def __init__(self, ws):
        self.ws = ws
        self.connected = True
    
    async def send_printer_info(ws: websockets.ClientConnection):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{RELAY_URL}", # Just for testing
                    headers={"Content-Type": "application/json"},
                    json={"info": "Printer information"}
                ) as response:
                    if response.status == 200:
                        print("Printer info sent successfully")
                    else:
                        print(f"Failed to send printer info: {response.status}")
        except Exception as e:
            print(f"Error: {e}")

async def main():
    async with websockets.connect(RELAY_URL) as ws:
        try:
            print("Connected to relay")
            asyncio.create_task(handle_messages(ws))
        except websockets.ConnectionClosed:
            print("Connection closed")

if __name__ == "__main__":
    asyncio.run(main())
