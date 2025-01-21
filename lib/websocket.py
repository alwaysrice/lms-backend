
from typing import Callable
from fastapi import WebSocket


class WebSocketWrapper:
    id: int
    socket: WebSocket


class ConnectionManager():
    def __init__(self):
        self.active_connections: list[WebSocketWrapper] = []

    async def connect(self, websocket: WebSocket, id: int = -1):
        await websocket.accept()
        socket = WebSocketWrapper()
        socket.id = id
        socket.socket = websocket
        self.active_connections.append(socket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_json(self, json: any):
        for connection in self.active_connections:
            await connection.socket.send_json(json)
