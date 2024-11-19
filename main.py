from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from lib.db import prisma
from routers import auth
from decouple import config
from models.request import TaskSubmissionRequestBody, ReactRequestBody, CommentRequestBody, CreatePostRequestBody


@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()

origins = [
    config("URL")
]
app = FastAPI(lifespan=lifespan)
app.include_router(auth.app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/get/teachers")
async def get_teachers():
    teachers = await prisma.users.find_many(where={"role": "TEACHER"})
    return teachers


@app.get("/get/admins")
async def get_admins():
    admins = await prisma.users.find_many(where={"role": "ADMIN"})
    return admins


@app.get("/get/students")
async def get_students():
    students = await prisma.users.find_many(where={"role": "STUDENT"})
    return students


@app.get("/get/user/{user_id}/")
async def get_user(user_id, groups: bool = False, tasks: bool = False):
    user = await prisma.user.find_unique(
        where={"id": user_id},
        include={
            "member_groups": groups,
            "admin_groups": groups,
            "tasks": tasks,
            "notifications": True,
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


@app.post("/create/task")
async def create_task():
    await prisma.task.create(
        data={

        }
    )


@app.get("/get/community")
async def get_community():
    items = await prisma.post.find_many(
        include={
            "source": True,
            "group": True,
            "reacts": True,
            "comments": {
                "include": {
                    "user": True,
                    "parent": True,
                    "replies": True,
                }
            }
        }
    )
    return items


@app.get("/get/post/{id}/")
async def get_post(id: int, reacts: bool = True, comments: bool = True):
    item = await prisma.post.find_unique(
        where={"id": id},
        include={
            "source": True,
            "group": True,
            "reacts": reacts,
            "comments": {
                "include": {
                    "user": True,
                    "parent": True,
                    "replies": True,
                }
            }
        })
    return item


@app.get("/get/task/{id}/")
async def get_task(id: int, assigned_users: bool = True, assigned_groups: bool = False, submissions: bool = False):
    item = await prisma.task.find_unique(
        where={"id": id},
        include={
            "assigned_users": assigned_users,
            "assigned_groups": assigned_groups,
            "task_submissions": submissions,
            "creator": True,
            "comments": {
                "include": {
                    "user": True,
                    "parent": True,
                    "replies": True,
                }
            }
        })
    return item


@app.get("/from/task-submission/{task}/{user}")
async def from_task_submission(task: int, user: int):
    item = await prisma.tasksubmission.find_first(
        where={"userId": user, "source_id": task})
    return item


@app.get("/get/groups/{group_type}")
async def get_group(group_type: str):
    return await prisma.group.find_many(where={"type": group_type})


@ app.get("/get/group/{id}/")
async def get_group(id: int, members: bool = True, posts: bool = False, tasks: bool = False):
    item = await prisma.group.find_first(
        where={"id": id},
        include={
            "posts": {
                "include": {
                    "source": True,
                    "group": True,
                    "reacts": True,
                    "comments": True,
                }
            },
            "tasks": tasks,
            "admins": members,
            "members": members,
        })
    return item


@ app.delete("/delete/comment/{id}/")
async def delete_comment(id: int):
    return await prisma.comment.delete(where={"id": id})


@ app.post("/post/comment")
async def post_comment(body: CommentRequestBody):
    return await prisma.comment.create(
        data={
            "post_id": body.post,
            "user_id": body.user,
            "content": body.text,
        }
    )


@ app.post("/task/comment")
async def task_comment(body: CommentRequestBody):
    return await prisma.taskcomment.create(
        data={
            "task_id": body.post,
            "user_id": body.user,
            "content": body.text,
        }
    )


@ app.post("/create/post")
async def create_post(body: CreatePostRequestBody):
    return await prisma.post.create(
        data={
            "user_id": body.source,
            "group_id": body.group,
            "title": body.title,
            "desc": body.desc,
            "cover_img": body.cover,
            "attachments": body.attachments,
        }
    )


@ app.post("/post/is/favorited")
async def post_is_favorited(body: ReactRequestBody):
    return await prisma.post.find_first(
        where={
            "id": body.post,
            "favorited_by": {
                "some": {
                    "id": body.user,
                }
            }
        }
    )


@ app.post("/post/has/reaction")
async def post_has(body: ReactRequestBody):
    return await prisma.postreaction.find_first(
        where={
            "postId": body.post,
            "userId": body.user,
        }
    )


@ app.post("/post/favorite")
async def post_favorite(body: ReactRequestBody):
    is_favorited = await prisma.post.find_first(
        where={
            "id": body.post,
            "favorited_by": {
                "some": {
                    "id": body.user,
                }
            }
        }
    )

    if is_favorited:
        await prisma.post.update(
            where={"id": body.post},
            data={
                "favorited_by": {
                    "disconnect": [{"id": body.user}],
                }
            })
    else:
        await prisma.post.update(
            where={"id": body.post},
            data={
                "favorited_by": {
                    "connect": [{"id": body.user}],
                }
            })


@ app.post("/post/react")
async def post_react(body: ReactRequestBody):
    existing_react = await prisma.postreaction.find_first(
        where={
            "postId": body.post,
            "userId": body.user,
            "reaction": body.reaction,
        }
    )
    if existing_react:
        if existing_react.reaction == body.reaction:
            await prisma.postreaction.delete(where={"id": existing_react.id})

        await prisma.postreaction.update(
            where={"id": existing_react.id},
            data={"reaction": body.reaction}
        )
    else:
        await prisma.postreaction.create(
            data={
                "postId": body.post,
                "userId": body.user,
                "reaction": body.reaction,
            }
        )
    return existing_react


@ app.post("/post/submission")
async def submit_task(body: TaskSubmissionRequestBody):
    item = await prisma.tasksubmission.create(
        data={
            "desc": body.remark,
            "attachments": body.attachments,
            "source_id": body.source,
            "userId": body.user,
        }
    )
    return item


@ app.post("/delete/user")
async def delete_user():
    await prisma.users.delete(
        data={

        }
    )
