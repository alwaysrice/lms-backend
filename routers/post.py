
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from lib.db import prisma
from routers.group import group_active
from models.request import ReactRequestBody, CreatePostRequestBody, Pair


app = APIRouter(
    tags=["post"]
)

socket = group_active

@app.get("/get/posts/group/{group_id}/")
async def get_posts_from_group(
        group_id: int,
        source: bool = True,
        group: bool = True,
        reacts: bool = True,
        comments: bool = True):
    item = await prisma.post.find_many(
        where={
            "group_id": group_id,
        },
        include={
            "source": source,
            "group": group,
            "reacts": reacts,
            "comments": comments,
        }
    )
    return item


@app.get("/get/resources/group/{group_id}/")
async def get_resources_from_group(
        group_id: int,
        source: bool = True,
        group: bool = True,
        reacts: bool = True,
        comments: bool = True):
    # return await prisma.post.query_raw(
    #     f"""
    #     SELECT
    #         "Post".*,
    #         "Group".*,
    #         "User".*,
    #         COALESCE(jsonb_agg(DISTINCT "PostReaction".*), '[]'::jsonb) AS reacts,
    #         COALESCE(jsonb_agg(DISTINCT "Comment".*), '[]'::jsonb) AS comments
    #     FROM
    #         "Post"
    #     LEFT JOIN "User" ON "Post"."user_id" = "User"."id"
    #     LEFT JOIN "Group" ON "Post"."group_id" = "Group"."id"
    #     LEFT JOIN "Comment" ON "Comment"."post_id" = "Post"."id"
    #     LEFT JOIN "PostReaction" ON "PostReaction"."post_id" = "Post"."id"
    #     WHERE
    #         "Post"."group_id" = {group_id}
    #         AND "Post"."meta"::jsonb ? 'resource'
    #     GROUP BY
    #         "Post"."id",
    #         "User"."id",
    #         "Group"."id";
    #     """
    # )
    return await prisma.post.find_many(
        where={
            "group_id": group_id,
            "meta": {
                "path": ["resource"],
                "string_contains": ""
            }
        }
    )


@app.post("/set/meta/{post_id}")
async def set_meta(post_id: int, body: Pair):
    # await prisma.post.query_raw(
    #     'UPDATE "Post" SET "meta" = $1 WHERE "id" = $2', data, post_id
    # )
    return await prisma.post.update(
        where={
            "id": post_id
        },
        data={
            "meta": json.dumps({body.key: body.value})
        }
    )


# def serialize_json(row):
#     for key, value in row.dict().items

@app.post("/create/post")
async def create_post(body: CreatePostRequestBody):
    item = await prisma.post.create(
        data={
            "user_id": body.source,
            "group_id": body.group,
            "title": body.title,
            "desc": body.desc,
            "cover_img": body.cover,
            "attachments": body.attachments,
        },
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
    item.meta["type"] = "post"
    item = item.json()
    # item["created_at"] = item["created_at"].isoformat()
    # item["updated_at"] = item["updated_at"].isoformat()
    await socket.broadcast_json(item)
    return item


@app.post("/post/is/favorited")
async def post_is_favorited(body: ReactRequestBody):
    item = await prisma.post.find_first(
        where={
            "id": body.post,
            "favorited_by": {
                "some": {
                    "id": body.user,
                }
            }
        }
    )
    if not item:
        return False
    return item


@app.post("/post/has/reaction")
async def post_has(body: ReactRequestBody):
    item = await prisma.postreaction.find_first(
        where={
            "post_id": body.post,
            "user_id": body.user,
        }
    )
    if not item:
        print("NOT LIKED")
        return False
    print("LIKED " + item.reaction)
    return item


@app.post("/post/favorite")
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


@app.post("/post/react")
async def post_react(body: ReactRequestBody):
    existing_react = await prisma.postreaction.find_first(
        where={
            "post_id": body.post,
            "user_id": body.user,
        }
    )
    if existing_react:
        if existing_react.reaction == body.reaction:
            await prisma.postreaction.delete(where={"id": existing_react.id})
            print("deleted Reaction: ")
        else:
            await prisma.postreaction.update(
                where={"id": existing_react.id},
                data={"reaction": body.reaction}
            )
            print("updated to: " + body.reaction)
    else:
        await prisma.postreaction.create(
            data={
                "post_id": body.post,
                "user_id": body.user,
                "reaction": body.reaction,
            }
        )
        print("created Reaction: " + body.reaction)
    return existing_react


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
