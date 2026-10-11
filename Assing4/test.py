
import asyncio
import websockets

async def handle_client(websocket):
    print("Client connected")

    try:
        async for message in websocket:
            print("Received:", message)
            await websocket.send(message)
    except websockets.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(
        handle_client, "localhost", 8765
    ):
        print("Test WebSocket server running on port 8765")
        await asyncio.Future()

asyncio.run(main())
