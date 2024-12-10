from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime
from lib.db import prisma
import asyncio

app = APIRouter(
    tags=["message"]
)

# @app.post("/send-message")
# async def send_message(sender_id, receiver_id, ):
#     items = await prisma.messageroom.find_many(where={
#         "participants": {
#             "every": {
#                 "id": user_id,
#             }
#         }
#     })
#     return items


class ConnectionManager():
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_json(self, json: any):
        for connection in self.active_connections:
            await connection.send_json(json)


manager = ConnectionManager()


@app.websocket("/chatroom")
async def chatroom_socket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # asyncio.create
            # message = data
            # if "typing" in data:
            #     await manager.broadcast_json({"typing": True})
            # else:
            message = await prisma.usermessage.create(data=data)
            message = message.dict()
            message["created_at"] = message["created_at"].isoformat()
            message["updated_at"] = message["updated_at"].isoformat()

            print("Received data")
            await manager.broadcast_json(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/get/chats/user/{user_id}")
async def get_user_chats(user_id):
    items = await prisma.messageroom.find_many(
        where={
            "participants": {
                "every": {
                    "id": user_id,
                }
            }
        },
        include={
            "messages": True,
            "participants": True,
        }
    )
    return items
