import asyncio
import websockets

async def handle_connection(websocket, path):
    print(f"Connection from {websocket.remote_address}")

    try:
        async for data in websocket:
            print(data, websocket)
            commands = data.split("\n")

            for command in commands:
                if command:
                    if command == "TURN_ON":
                        print("LED turned on")
                        # Code to turn on the LED
                    elif command == "TURN_OFF":
                        print("LED turned off")
                        # Code to turn off the LED
                    elif command == "HEARTBEAT":
                        print("Heartbeat")
                        await websocket.send("Connection OK")
                    elif command.startswith("ORDER:"):
                        # Extract the order data from the command
                        order_data = command.split(":")[1]
                        order_items = order_data.split(",")
                        print("Received order:")
                        for item in order_items:
                            print(f"  {item}")
                        # Send a confirmation back to the WebSocket client
                        response = "ORDER_CONFIRMED"
                        await websocket.send(response)
                    elif command == "QUIT":
                        print("Client has quit. Closing connection.")
                        break
                    else:
                        print("Invalid command")
    except websockets.ConnectionClosedError:
        print("WebSocket connection closed unexpectedly")
    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    ws_url = 'ws://127.0.0.1:8000/ws/raspberry_pi/'
    async with websockets.connect(ws_url) as websocket:
        await handle_connection(websocket, None)

if __name__ == "__main__":
    asyncio.run(main())
