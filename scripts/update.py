
import asyncio
from pprint import pprint
import numpy as np
import random
from prisma import Prisma
from faker import Faker
import randominfo
from datetime import timedelta, datetime
from prisma.bases import BaseUser
import bcrypt

fake = Faker()
prisma = Prisma()


async def main():
    await prisma.connect()

    await prisma.postreaction.delete_many()
    await prisma.comment.delete_many()
    await prisma.post.delete_many()
    await prisma.tasksubmission.delete_many()
    await prisma.taskresponse.delete_many()
    await prisma.message.delete_many()
    await prisma.taskcomment.delete_many()
    await prisma.task.delete_many()
    await prisma.notification.delete_many()
    await prisma.profile.delete_many()
    await prisma.group.delete_many()
    await prisma.user.delete_many()
    await prisma.disconnect()

asyncio.run(main())
