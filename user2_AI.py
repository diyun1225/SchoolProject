import asyncio
import websockets

async def client():
    uri = "ws://localhost:6789"  # 替換為伺服器地址
    async with websockets.connect(uri) as websocket:
        # 傳送身份
        await websocket.send("AI")
        print("Connected to the server as AI!")

        async def receive_messages():
            while True:
                message = await websocket.recv()
                print(f"Server: {message}")

        async def send_messages():
            while True:
                msg = input("AI: ")
                await websocket.send(msg)

        # 同時執行接收和發送
        await asyncio.gather(receive_messages(), send_messages())

if __name__ == "__main__":
    asyncio.run(client())
