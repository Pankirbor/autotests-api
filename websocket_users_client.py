import asyncio
import json

import websockets


async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as ws:
        print("Подключено к серверу. Введите сообщения (или 'exit' для выхода):")

        async def recive_messages():
            try:
                async for message in ws:
                    message = json.loads(message)
                    client_id = message.get("client_id")
                    client_msg = message.get("message")
                    print(
                        f"[Сообщение пользователя {client_id}]:\n {client_msg}",
                        end="\n> ",
                    )
            except websockets.exceptions.ConnectionClosed:
                print("\nСоединение с сервером разорвано")

        asyncio.create_task(recive_messages())

        while True:
            message = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
            if message == "exit":
                break
            await ws.send(message)


asyncio.run(client())
