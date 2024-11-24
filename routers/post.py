
from fastapi import APIRouter
import json
from lib.db import prisma
from models.request import ReactRequestBody, CreatePostRequestBody, Pair


app = APIRouter(
    tags=["post"]
)


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


@app.post("/create/post")
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


@app.post("/post/is/favorited")
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


@app.post("/post/has/reaction")
async def post_has(body: ReactRequestBody):
    return await prisma.postreaction.find_first(
        where={
            "post_id": body.post,
            "user_id": body.user,
        }
    )


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
                "post_id": body.post,
                "user_id": body.user,
                "reaction": body.reaction,
            }
        )
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
