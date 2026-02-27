import asyncio
import websockets

async def test_ws():
    uri = "ws://127.0.0.1:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")
            await websocket.send("Hello")
            print("Message sent")
            # Wait a sec
            await asyncio.sleep(1)
            print("Connection successful and alive")
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(test_ws())
