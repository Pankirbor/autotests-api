import pytest_asyncio
import websockets

from websocket_users_server import client_handler


@pytest_asyncio.fixture
async def websocket_server():
    async with websockets.serve(client_handler, "localhost", 8765) as server:
        yield server
        server.close()
        await server.wait_closed()


@pytest_asyncio.fixture
async def websocket_client():
    async with websockets.connect("ws://localhost:8765") as ws:
        yield ws
