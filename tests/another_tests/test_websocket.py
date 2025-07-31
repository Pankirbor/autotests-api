import asyncio
import json

import pytest


@pytest.mark.asyncio
async def test_message_exchange(websocket_server, websocket_client):
    test_message = "Hello, WebSocket!"
    responses = []

    # Отправляем сообщение
    await websocket_client.send(test_message)

    for _ in range(5):
        response = await websocket_client.recv()
        responses.append(json.loads(response).get("messages"))

    assert len(responses) == 5
    assert len(set(responses)) == 1

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(websocket_client.recv(), timeout=0.1)
