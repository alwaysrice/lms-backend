from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from lib.db import prisma
from lib.websocket import ConnectionManager

app = APIRouter(
    tags=["message"]
)

manager = ConnectionManager()


@app.websocket("/chatroom")
async def chatroom_socket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
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
