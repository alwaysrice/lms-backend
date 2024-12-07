

from fastapi import APIRouter
from lib.db import prisma


app = APIRouter(
    tags=["comment"]
)


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
