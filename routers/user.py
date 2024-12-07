from fastapi import APIRouter
from lib.db import prisma
from models.request import DictModel

app = APIRouter(
    tags=["user"]
)


@app.get("/get/users/")
async def get_users(role: str):
    items = await prisma.user.find_many(where={"role": role})
    return items


@app.get("/get/teachers")
async def get_teachers():
    teachers = await prisma.user.find_many(where={"role": "TEACHER"})
    return teachers


@app.get("/get/admins")
async def get_admins():
    admins = await prisma.user.find_many(where={"role": "ADMIN"})
    return admins


@app.get("/get/students")
async def get_students():
    students = await prisma.user.find_many(where={"role": "STUDENT"})
    return students


@app.put("/update/user/{user_id}/")
async def udpate_user(user_id: int, body: DictModel):
    user = await prisma.user.update(
        where={"id": user_id},
        data=body.dict)
    return user


@app.put("/update/profile/{user_id}/")
async def udpate_profile(user_id: int, body: DictModel):
    print("Updating profile" + str(body.data))
    profile = await prisma.profile.update(
        where={"id": user_id},
        data=body.data)
    return profile


@app.get("/get/user/{user_id}/")
async def get_user(user_id, groups: bool = False, tasks: bool = False):
    user = await prisma.user.find_first(
        where={"id": user_id},
        include={
            "member_groups": groups,
            "admin_groups": groups,
            "tasks": tasks,
            "notifications": True,
            "profile": True,
        })
    return user


@app.get("/get/user/by-username/{username}/")
async def get_user_by_username(username, groups: bool = False, tasks: bool = False):
    user = await prisma.user.find_first(
        where={"username": username},
        include={
            "member_groups": groups,
            "admin_groups": groups,
            "tasks": tasks,
            "notifications": True,
            "profile": True,
        })
    return user


@app.get("/get/logged-user")
async def get_logged_user():

    user = await prisma.users.find_unique(where={"username": ""})
    return user


@app.post("/create/user")
async def create_user():
    await prisma.users.create(
        data={

        }
    )


@app.post("/delete/user")
async def delete_user():
    await prisma.users.delete(
        data={

        }
    )
