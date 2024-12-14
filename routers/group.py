

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from lib.db import prisma
from lib.websocket import ConnectionManager


app = APIRouter(
    tags=["comment"]
)


group_active = ConnectionManager()


@app.websocket("/group-active")
async def post_feed_socket(websocket: WebSocket):
    await group_active.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            message = data
            print("Received data")
            await group_active.broadcast_json(message)
    except WebSocketDisconnect:
        group_active.disconnect(websocket)


@app.get("/get/groups/{group_type}")
async def get_groups(group_type: str):
    return await prisma.group.find_many(where={"type": group_type})


@app.get("/get/group/{id}/")
async def get_group(
        id: int,
        members: bool = True,
        posts: bool = False,
        tasks: bool = False):
    item = await prisma.group.find_first(
        where={"id": id},
        include={
            "posts": posts,
            "tasks": tasks,
            "admins": members,
            "members": members,
        })
    return item


@app.get("/get/school/")
async def get_school():
    item = await prisma.group.find_first(
        where={"name": "Gray University"},
        include={
            "posts": True,
            "tasks": True,
            "admins": True,
            "members": True,
        })
    return item
