
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

    users = await prisma.user.find_many()

    for user in users:
        for i in range(random.randint(3, 20)):
            await prisma.message.create(data={
                "content": fake.text(20),
                "receiver_id": random.choice(users).id,
                "user_id": user.id,
            })

    await prisma.disconnect()

asyncio.run(main())
