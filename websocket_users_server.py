import asyncio
import json
from datetime import datetime

import websockets

connected_clients = set()


async def broadcast(message: dict[str, str], lock: asyncio.Lock, exclude=None):
    async with lock:
        for client in list(connected_clients):
            if client != exclude:
                try:
                    await client.send(message)
                    await asyncio.sleep(0.05)
                except websockets.exceptions.ConnectionClosed:
                    connected_clients.discard(client)
                    print(
                        f"[{datetime.now().time()}] Клиент {id(client)} отключен. Осталось: {len(connected_clients)}"
                    )


async def client_handler(websocket: websockets.ServerConnection):
    lock = asyncio.Lock()

    async with lock:
        connected_clients.add(websocket)

    client_id = id(websocket)
    print(
        f"[{datetime.now().time()}] Новый клиент: {client_id}. Всего: {len(connected_clients)}"
    )

    try:
        async for message in websocket:
            print(f"Сообщение пользователя {client_id}: {message}")
            server_msg = {"client_id": client_id, "message": message}
            tasks = [broadcast(json.dumps(server_msg), lock) for _ in range(5)]
            await asyncio.gather(*tasks)

    except websockets.exceptions.ConnectionClosed:
        print(f"[{datetime.now().time()}] Клиент {client_id} отключился")
        async with lock:
            connected_clients.discard(websocket)
            print(
                f"[{datetime.now().time()}] Клиент {client_id} отключен. Осталось: {len(connected_clients)}"
            )

    # finally:
    #     if websocket in connected_clients:
    #         connected_clients.remove(websocket)
    #     print(
    #         f"[{datetime.now().time()}] Клиент {client_id} отключен. Осталось: {len(connected_clients)}"
    #     )


async def main():
    server = await websockets.serve(client_handler, "localhost", 8765)
    print(f"Сервер запущен на ws://localhost:8765")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
