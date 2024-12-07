
import json
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
import os

fake = Faker()
prisma = Prisma()


async def main():
    await prisma.connect()

    admin = await prisma.user.find_first(where={"username": "admin"})
    school = await prisma.group.find_first(where={"name": "Gray University"})
    for i in range(random.randint(3, 10)):
        await prisma.post.create(data={
            "desc": fake.text(),
            "title": fake.text(random.randint(5, 30)),
            "cover_img": "https://loremflickr.com/200/200?random=1",
            "user_id": admin.id,
            "group_id": school.id,
            "meta": json.dumps({
                "type": "staff", 
            }),
        })

    await prisma.disconnect()

asyncio.run(main())
