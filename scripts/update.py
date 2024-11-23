
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

    submissions = await prisma.tasksubmission.find_many()
    for submission in submissions:
        await prisma.taskstate.create(data={
            "user_id": submission.userId,
            "source_id": submission.source_id,
        })
    await prisma.disconnect()

asyncio.run(main())
