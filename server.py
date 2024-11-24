import asyncio
import websockets

# 用於儲存連線的用戶與其身份
connected_users = {}

async def handler(websocket):
    try:
        # 接收客戶端傳來的身份訊息
        identity = await websocket.recv()
        connected_users[websocket] = identity
        print(f"{identity} connected.")

        # 廣播新用戶加入訊息
        for user in connected_users:
            if user != websocket:
                await user.send(f"{identity} has joined the chat.")

        # 接收訊息並廣播
        async for message in websocket:
            print(f"Message from {identity}: {message}")
            # 廣播給所有其他用戶
            for user in connected_users:
                if user != websocket:  # 不回傳給發送者
                    await user.send(f"{identity}: {message}")

    except websockets.ConnectionClosed:
        print(f"{connected_users[websocket]} disconnected.")
    finally:
        # 當用戶斷開連線，移除記錄並通知其他用戶
        if websocket in connected_users:
            disconnected_user = connected_users.pop(websocket)
            for user in connected_users:
                await user.send(f"{disconnected_user} has left the chat.")

async def main():
    print("WebSocket server running on ws://0.0.0.0:6789")
    async with websockets.serve(handler, "0.0.0.0", 6789):
        await asyncio.Future()  # 保持伺服器持續運行

if __name__ == "__main__":
    asyncio.run(main())
