from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from lib.db import prisma
from routers import auth, task, comment, group, user, post
from decouple import config


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
app.include_router(task.app)
app.include_router(post.app)
app.include_router(user.app)
app.include_router(group.app)
app.include_router(comment.app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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
