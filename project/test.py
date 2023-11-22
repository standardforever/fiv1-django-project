import asyncio
import websockets

async def connect_to_websocket(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                append_message(data)
            except websockets.ConnectionClosed:
                print("WebSocket closed unexpectedly")

def append_message(data):
    formatted_message = "Received Data:<br>"

    for key, value in data.items():
        formatted_message += f"<strong>{key}:</strong> {value}<br>"

    print(formatted_message)

if __name__ == "__main__":
    import json

    uri = "ws://127.0.0.1:8000/ws/raspberry_pi/"  # Replace with your WebSocket URI
    asyncio.get_event_loop().run_until_complete(connect_to_websocket(uri))
