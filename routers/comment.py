
from fastapi import APIRouter
from lib.db import prisma
from models.request import CommentRequestBody


app = APIRouter(
    tags=["comment"]
)


@app.post("/task/comment")
async def task_comment(body: CommentRequestBody):
    return await prisma.taskcomment.create(
        data={
            "task_id": body.post,
            "user_id": body.user,
            "content": body.text,
        }
    )


@app.put("/update/task/comment")
async def update_task_comment(body: CommentRequestBody):
    return await prisma.taskcomment.create(
        where={
            "task_id": body.post,
            "user_id": body.user,
        },
        data={
            "content": body.text,
        }
    )


@app.delete("/delete/task/comment/{id}/")
async def delete_task_comment(id: int):
    return await prisma.taskcomment.delete(where={"id": id})


@app.delete("/delete/comment/{id}/")
async def delete_comment(id: int):
    return await prisma.comment.delete(where={"id": id})


@app.post("/post/comment")
async def post_comment(body: CommentRequestBody):
    return await prisma.comment.create(
        data={
            "post_id": body.post,
            "user_id": body.user,
            "content": body.text,
        }
    )


@app.put("/update/comment")
async def update_comment(body: CommentRequestBody):
    return await prisma.comment.create(
        where={
            "post_id": body.post,
            "user_id": body.user,
        },
        data={
            "content": body.text,
        }
    )
