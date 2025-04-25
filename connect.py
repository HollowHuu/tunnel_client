import asyncio
import websockets
from websockets.asyncio.client import connect
import aiohttp
import json

import moonraker

RELAY_URL = "ws://localhost:9001"
MOONRAKER_URL = "ws://localhost:7125/klippysocket"


class ServerConnection:
    def __init__(self):
        self.connected = True

    async def send_printer_info(self, ws: websockets.ClientConnection):
        print("Sending printer info...")
        try:
            # Simulate sending printer info
            printer_info = {
                "status": "online",
                "temperature": 200,
                "progress": 50
            }
            await ws.send(json.dumps(printer_info))
            print("Printer info sent")

            message = await ws.recv()
            print(f"Received message: {message}")
        except Exception as e:
            print(f"Error: {e}")

async def main():


    moonraker_connection = moonraker.Moonraker(MOONRAKER_URL)
    moonraker_task = asyncio.create_task(moonraker_connection.connect())
    await moonraker_task

    moonraker_task = asyncio.create_task(moonraker_connection.listen())
    await moonraker_task

    async with connect(RELAY_URL) as ws:
        await ws.send("Hello from client")
        try:
            server_connection = ServerConnection()
            print("Connected to relay")
            task = asyncio.create_task(server_connection.send_printer_info(ws))
            await task
        except websockets.ConnectionClosed:
            print("Connection closed")

if __name__ == "__main__":
    asyncio.run(main())
