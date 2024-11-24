import asyncio
import json
import pytz
from pprint import pprint
import numpy as np
import random
from prisma import Prisma
from faker import Faker
import randominfo
from datetime import timedelta, datetime, timezone
from prisma.bases import BaseUser
import bcrypt

fake = Faker()
prisma = Prisma()


def faker_text(length):
    generated_text = ''

    while len(generated_text) < length:
        generated_text += fake.text(max_nb_chars=100) + ' '

    return generated_text[:length]


def ranchance(percent=50):
    return random.randint(0, 99) < percent


def faker_duedate(min=1, max=30):
    days_to_add = fake.random_int(min=min, max=max)
    if ranchance():
        return datetime.now() - timedelta(days=days_to_add)
    return datetime.now() + timedelta(days=days_to_add)


async def fake_users(num=1, seed=None):
    np.random.seed(seed)
    fake.seed_instance(seed)
    for x in range(num):
        gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
        first_name = fake.first_name_male() if gender == "M" else fake.first_name_female()
        last_name = fake.last_name()

        await prisma.user.create(data={
            "firstname": first_name,
            "lastname": last_name,
            "username": f"{last_name.lower()}{first_name.lower()}_{random.randint(0, 9)}{random.randint(0, 99)}",
            "email": f"{last_name.lower()}.{first_name.lower()}@{fake.domain_name()}",
            "password": bcrypt.hashpw("zxcv".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            "role": random.choice(["STUDENT", "TEACHER", "ADMIN"])
        })


    student = await prisma.user.create(data={
        "firstname": "John",
        "lastname": "Pascal",
        "username": "student",
        "email": "pascaljohn@gmail.com",
        "password": bcrypt.hashpw("zxcv".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "role": "STUDENT"
    })
    await prisma.profile.create(data={
        "user_id": student.id,
    })
    await prisma.usersettings.create(data={
        "user_id": student.id,
    })
    await prisma.user.create(data={
        "firstname": "Richard",
        "lastname": "Gordon",
        "username": "teacher",
        "email": "gordssa@yahoo.com",
        "password": bcrypt.hashpw("zxcv".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "role": "TEACHER"
    })
    await prisma.user.create(data={
        "firstname": "Thomas",
        "lastname": "Dominis",
        "username": "admin",
        "email": "thos@gmail.com",
        "password": bcrypt.hashpw("zxcv".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "role": "ADMIN"
    })
    return await prisma.user.find_many()


async def getIds(query):
    return [item.id for item in query]


async def fake_groups(admins: list, members: list, seed=None):
    np.random.seed(seed)
    fake.seed_instance(seed)
    classes = [
        "Math",
        "Philosopy",
        "Read & Writing",
        "General Biology",
        "Understanding Culture Society and Politics",
        "Physical Education",
    ]

    institution = [
        ["Prime News Club", "CLUB"],
        ["Uni Highschool Department", "INSTITUTION"],
        ["Uni Accounting Department", "INSTITUTION"],
        ["Gray University", "INSTITUTION"],
    ]
    others = [
        ["Supreme Student(SS)", "ORGANIZATION"],
    ]

    for x in range(len(others)):
        await prisma.group.create(data={
            "name": others[x][0],
            "desc": fake.text(),
            "type": others[x][1],
            "year_start": datetime.now(),
            "admins": {"connect": [{"id": admins.pop()}]},
            "members": {"connect": [{"id": id} for id in random.sample(members, random.randint(int(len(members)/2), len(members)))]}
        })
    for x in range(len(institution)):
        await prisma.group.create(data={
            "name": institution[x][0],
            "desc": fake.text(),
            "type": institution[x][1],
            "year_start": datetime.now(),
            "meta": json.dumps({"branch": "Candelaria"}),
            "admins": {"connect": [{"id": admins.pop()}]},
            "members": {"connect": [{"id": id} for id in random.sample(members, random.randint(int(len(members)/2), len(members)))]}
        })
    for x in range(len(classes)):
        await prisma.group.create(data={
            "name": classes[x],
            "desc": fake.text(),
            "type": "CLASS",
            "year_start": datetime.now(),
            "year_end": datetime.now() + timedelta(days=365),
            "admins": {"connect": [{"id": admins.pop()}]},
            "members": {"connect": [{"id": id} for id in random.sample(members, random.randint(int(len(members)/2), len(members)))]}
        })

    groups = await getIds(await prisma.group.find_many())
    for x in range(random.randint(3*len(groups), 10*len(groups))):
        random_groups = random.sample(groups, random.randint(3, 8))
        all_group_members = []

        for z in random_groups:
            all_group_members.extend(await getIds(await prisma.user.find_many(where={"member_groups": {"some": {"id": z}}})))

        creator = await prisma.user.find_first(where={"admin_groups": {"some": {"id": random.choice(random_groups)}}})
        creator = creator.id
        await prisma.task.create(data={
            "name": faker_text(random.randint(10, 40)),
            "desc": faker_text(random.randint(100, 500)) if random.random() < 30/100 else "",
            "assigned_users": {
                "connect": [{"id": id} for id in all_group_members]
            },
            "assigned_groups": {
                "connect": [{"id": id} for id in random_groups]
            },
            "creator_id": creator,
            "due_at": faker_duedate()
        })

    tasks = await getIds(await prisma.task.find_many())
    for y in tasks:
        assigned_to = await getIds(await prisma.user.find_many(where={"tasks": {"some": {"id": y}}}))
        task = await prisma.task.find_unique(where={"id": y})
        for x in assigned_to:
            if datetime.now(timezone.utc) >= task.due_at:
                await prisma.tasksubmission.create(data={
                    "desc": faker_text(random.randint(100, 500)) if random.random() < 30/100 else "",
                    "attachments": ["file-export.pdf", "proof.docx"],
                    "source_id": y,
                    "user_id": x,
                })
                await prisma.taskresponse.create(data={
                    "source_id": y,
                    "user_id": x,
                    "grade": random.randint(60, 99)
                })
        for x in range(random.randint(int(len(assigned_to)/2), len(assigned_to))):
            await prisma.tasksubmission.create(data={
                "desc": faker_text(random.randint(100, 500)) if random.random() < 30/100 else "",
                "source_id": y,
                "user_id": assigned_to.pop(),
            })

    for x in range(random.randint(3, 30)):
        await prisma.taskcomment.create(data={
            "content": fake.text(),
            "user_id": random.choice(members),
            "task_id": random.choice(tasks)
        })

    return await prisma.group.find_many()


async def fake_posts(users: list, groups: list, num=100, seed=None):
    np.random.seed(seed)
    fake.seed_instance(seed)
    for x in range(num):
        await prisma.post.create(data={
            "desc": fake.text(),
            "title": fake.text(random.randint(5, 30)),
            "cover_img": "https://loremflickr.com/200/200?random=1" if random.random() < 20/100 else "",
            "user_id": random.choice(users),
            "group_id": random.choice(groups),
        })

    posts = await getIds(await prisma.post.find_many())
    for x in range(random.randint(3, 30)):
        await prisma.comment.create(data={
            "content": fake.text(),
            "user_id": random.choice(users),
            "post_id": random.choice(posts)
        })

    for post in posts:
        users_copy = users.copy()
        random.shuffle(users_copy)
        for x in range(random.randint(3, len(users))):
            await prisma.postreaction.create(
                data={
                    "reaction": random.choice(["LIKE", "FUNNY", "SAD", "ANGRY"]),
                    "user_id": users_copy.pop(),
                    "post_id": post
                }
            )


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
    await prisma.usersettings.delete_many()
    await prisma.sitetheme.delete_many()
    await prisma.posttag.delete_many()
    await prisma.profilebadge.delete_many()
    await prisma.group.delete_many()
    await prisma.user.delete_many()

    users = await fake_users(100)
    admins = await getIds(list(filter(lambda user: user.role == "TEACHER", users)))
    students = await getIds(list(filter(lambda user: user.role == "STUDENT", users)))
    groups = await fake_groups(admins, students)
    posts = await fake_posts(await getIds(users), await getIds(groups))
    await prisma.disconnect()

asyncio.run(main())
