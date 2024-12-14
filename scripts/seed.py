import asyncio
import json
import numpy as np
import random
from prisma import Prisma
from faker import Faker
from datetime import timedelta, datetime, timezone
import bcrypt
import os

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
        return datetime.now(timezone.utc) - timedelta(days=days_to_add)
    return datetime.now(timezone.utc) + timedelta(days=days_to_add)


student = None


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

    global student
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
    dean = await prisma.user.create(data={
        "firstname": "Burger",
        "lastname": "King",
        "middlename": "Angels",
        "suffix": "II",
        "username": "dean",
        "email": "dean@uni.com",
        "password": bcrypt.hashpw("zxcv".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "role": "ADMIN",
        "pfp": "static/images/dean.jpg"
    })
    for i in os.listdir("static/images/teachers"): 
        await prisma.user.create(data={
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "username": fake.user_name(),
            "email": fake.email(),
            "password": bcrypt.hashpw("zxcv".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            "role": "TEACHER",
            "pfp": "static/images/teachers/" + i
        })
# user in filter(lambda user: user.id != student, users)]

    users = await prisma.user.find_many()
    rooms = []
    for i in range(random.randint(int(len(users)/2), len(users))):
        item = await prisma.messageroom.create(data={
            "participants": {
                "connect": [{"id": user.id} for user in users],
            }
        })
        rooms.append(item)

    for room in list(filter(lambda _: ranchance(40), rooms)):
        for i in range(random.randint(100, 200)):
            trade = {}
            if ranchance(20):
                trade = {
                    "user_id": student.id,
                    "receiver_id": random.choice(users).id,
                }
            else:
                trade = {
                    "user_id": random.choice(users).id,
                    "receiver_id": student.id,
                }
            await prisma.usermessage.create(data={
                **trade,
                "room_id": room.id,
                "content": fake.sentence(),
            })

    return users


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
        ["Uni Highschool Department", "INSTITUTION"],
        ["Uni Accounting Department", "INSTITUTION"],
        ["Gray University", "INSTITUTION"],
    ]
    others = [
        ["Prime News Club", "CLUB"],
        ["Supreme Student(SS)", "ORGANIZATION"],
    ]

    for x in range(len(others)):
        await prisma.group.create(data={
            "name": others[x][0],
            "desc": fake.text(),
            "type": others[x][1],
            "year_start": datetime.now(),
            "admins": {"connect": [{"id": admins.pop().id}]},
            "members": {"connect": [{"id": user.id} for user in random.sample(members, random.randint(int(len(members)/2), len(members)))]}
        })
    for x in range(len(institution)):
        await prisma.group.create(data={
            "name": institution[x][0],
            "desc": fake.text(),
            "type": institution[x][1],
            "year_start": datetime.now(),
            "meta": json.dumps({
                "branch": "Candelaria",
                "location": "Malabanban Norte Candelaria, Quezon",
            }),
            "admins": {"connect": [{"id": admins.pop().id}]},
            "members": {"connect": [{"id": user.id} for user in random.sample(members, random.randint(int(len(members)/2), len(members)))]}
        })
    classes_data = []
    await prisma.group.create(
        data={
            "id": -1,
            "name": "Public",
            "desc": "",
            "type": "CASUAL",
            "year_start": datetime.now(),
        }
    )
    for x in range(len(classes)):
        item = await prisma.group.create(
            data={
                "name": classes[x],
                "desc": fake.text(),
                "type": "CLASS",
                "year_start": datetime.now(),
                "year_end": datetime.now() + timedelta(days=365),
                "admins": {"connect": [{"id": admins.pop().id}]},
                "members": {"connect": [{"id": user.id} for user in random.sample(members, random.randint(int(len(members)/2), len(members)))]}
            },
            include={
                "members": True,
                "admins": True,
            }
        )
        classes_data.append(item)

    task_count_min = 40
    task_count_max = 100
    tasks = []
    for i in range(random.randint(task_count_min, task_count_max)):
        classes_list = list(filter(lambda _: ranchance(80), classes_data))
        for class_item in classes_list:
            creator = random.choice(class_item.admins)
            item = await prisma.task.create(
                data={
                    "name": faker_text(random.randint(10, 40)),
                    "desc": faker_text(random.randint(100, 500)) if random.random() < 30/100 else "",
                    "assigned_users": {
                        "connect": [{"id": member.id} for member in class_item.members]
                    },
                    "assigned_groups": {
                        "connect": [{"id": class_item.id}]
                    },
                    "creator_id": creator.id,
                    "due_at": faker_duedate()
                },
                include={
                    "assigned_users": True,
                }
            )
            tasks.append(item)

    for task in random.sample(tasks, random.randint(int(len(tasks)/3), len(tasks))):
        assigned = list(filter(lambda _: ranchance(), task.assigned_users)) + [student]
        for assigned_user in assigned:
            if datetime.now(timezone.utc) >= task.due_at:
                await prisma.tasksubmission.create(data={
                    "desc": fake.paragraph(random.randint(1, 3)) if random.random() < 30/100 else "",
                    "attachments": [fake.file_name()],
                    "source_id": task.id,
                    "user_id": assigned_user.id,
                })
                if ranchance():
                    await prisma.taskresponse.create(data={
                        "source_id": task.id,
                        "user_id": assigned_user.id,
                        "grade": random.randint(60, 99)
                    })

    for i in range(random.randint(3, 30)):
        await prisma.taskcomment.create(data={
            "content": fake.text(),
            "user_id": random.choice(members).id,
            "task_id": random.choice(tasks).id,
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
            "user_id": random.choice(users).id,
            "group_id": random.choice(groups).id,
        })

    posts = await prisma.post.find_many()
    for x in range(random.randint(3, 30)):
        await prisma.comment.create(data={
            "content": fake.text(),
            "user_id": random.choice(users).id,
            "post_id": random.choice(posts).id
        })

    for post in posts:
        users_copy = users.copy()
        random.shuffle(users_copy)
        for x in range(random.randint(3, len(users))):
            await prisma.postreaction.create(
                data={
                    "reaction": random.choice(["LIKE", "FUNNY", "SAD", "ANGRY"]),
                    "user_id": users_copy.pop().id,
                    "post_id": post.id
                }
            )


async def main():
    await prisma.connect()

    await prisma.postreaction.delete_many()
    await prisma.comment.delete_many()
    await prisma.post.delete_many()
    await prisma.tasksubmission.delete_many()
    await prisma.taskresponse.delete_many()
    await prisma.usermessage.delete_many()
    await prisma.messageroom.delete_many()
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
    admins = list(filter(lambda user: user.role == "TEACHER", users))
    students = list(filter(lambda user: user.role == "STUDENT", users))
    groups = await fake_groups(admins, students)
    posts = await fake_posts(users, groups)
    await prisma.disconnect()

asyncio.run(main())
