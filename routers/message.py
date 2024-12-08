from fastapi import APIRouter
from lib.db import prisma

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
