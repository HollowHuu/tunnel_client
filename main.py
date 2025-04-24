import asyncio
import websockets
import aiohttp
import json

RELAY_URL = "ws://localhost:9001"
PRINTER_URL = "http://localhost:4408"

async def handle_request(ws, request):
    try:
        req = json.loads(request)
        url = f"{PRINTER_URL}{req['path']}"
        headers = req.get("headers", {})
        method = req["method"].upper()
        body = req.get("body", None)

        print(f"Handling request: {method} {url}")

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, data=body) as resp:
                response = {
                    "id": req["id"],
                    "status": resp.status,
                    "headers": dict(resp.headers),
                    "body": await resp.text()
                }
                await ws.send(json.dumps(response))
    except Exception as e:
        print(f"Error: {e}")

async def main():
    async with websockets.connect(RELAY_URL) as ws:
        print("Connected to relay")
        async for message in ws:
            asyncio.create_task(handle_request(ws, message))

if __name__ == "__main__":
    asyncio.run(main())
