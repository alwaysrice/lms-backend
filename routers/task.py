
from fastapi import APIRouter, HTTPException
from lib.db import prisma
from models.request import TaskSubmissionRequestBody, TaskGradeRequestBody
from datetime import datetime

app = APIRouter(
    tags=["task"]
)


@app.get("/get/tasks-responses/group/{group_id}")
async def get_tasks_responses_from_group(
        group_id: int,
        user_id: int,
        assigned_users: bool = True,
        assigned_groups: bool = False,
        submissions: bool = False):
    item = await prisma.task.find_many(
        where={
            "assigned_groups": {
                "some": {
                    "id": group_id,
                }
            },
        },
        include={
            "users_grade": {
                "where": {
                    "users_grade": {
                        "some": {
                            "user_id": user_id,
                        }
                    }
                }
            },
            "assigned_users": True,
            "assigned_groups": True,
            "task_submissions": True,
            "creator": True,
            "comments": {
                "include": {
                    "user": True,
                    "parent": True,
                    "replies": True,
                }
            }
        }
    )
    return item


@app.get("/is/task/missed")
async def check_if_missed(
        user_id: int,
        task_id: int):

    item = await prisma.task.find_first(
        where={
            "id": task_id,
            "due_at": {
                "lt": datetime.now()
            },
            "task_submissions": {
                "none": {
                    "user_id": user_id
                }
            },
        }
    )
    return item is not None


@app.get("/get/tasks-category/group/{group_id}")
async def get_user_tasks_from_group(
        group_id: int,
        user_id: int,
        category: str,
        assigned_users: bool = True,
        assigned_groups: bool = False,
        submissions: bool = False):
    filter = {}

    if category == "completed":
        filter = {
            "task_submissions": {
                "some": {
                    "user_id": user_id
                }
            },
        }
    elif category == "missed":
        filter = {
            "due_at": {
                "lt": datetime.now()
            },
            "task_submissions": {
                "none": {
                    "user_id": user_id
                }
            },
        }
    elif category == "due":
        filter = {
            "due_at": {
                "gt": datetime.now()
            },
            "assigned_users": {
                "some": {
                    "id": user_id
                }
            }
        }
    elif category == "graded":
        filter = {
            "users_grade": {
                "some": {
                    "user": {
                        "id": user_id
                    }
                }
            }
        }

    group_filter = {
        "assigned_groups": {
            "some": {
                "id": group_id,
            }
        },
    }
    if group_id == -99:
        group_filter = {}

    item = await prisma.task.find_many(
        where={
            **group_filter,
            **filter,
        },
        include={
            "users_grade": True,
            "assigned_users": True,
            "assigned_groups": True,
            "task_submissions": True,
            "creator": True,
            "comments": {
                "include": {
                    "user": True,
                    "parent": True,
                    "replies": True,
                }
            }
        }
    )
    return item


@app.get("/get/tasks/group/{group_id}")
async def get_tasks_from_group(
        group_id: int,
        assigned_users: bool = True,
        assigned_groups: bool = False,
        submissions: bool = False):
    item = await prisma.task.find_many(
        where={
            "assigned_groups": {
                "some": {
                    "id": group_id,
                }
            },
        },
        include={
            "users_grade": True,
            "assigned_users": True,
            "assigned_groups": True,
            "task_submissions": True,
            "creator": True,
            "comments": {
                "include": {
                    "user": True,
                    "parent": True,
                    "replies": True,
                }
            }
        }
    )
    return item


@app.get("/get/task/{id}/")
async def get_task(
        id: int,
        assigned_users: bool = True,
        assigned_groups: bool = False,
        submissions: bool = False):
    item = await prisma.task.find_unique(
        where={
            "id": id,
        },
        include={
            "users_grade": True,
            "assigned_users": assigned_users,
            "assigned_groups": assigned_groups,
            "task_submissions": submissions,
            "creator": True,
            "comments": {
                "include": {
                    "user": True,
                    "parent": True,
                    "replies": True,
                }
            }
        })
    return item


@app.get("/from/task-response/{task}/{user}")
async def from_task_response(task: int, user: int):
    item = await prisma.taskresponse.find_first(
        where={"user_id": user, "source_id": task})
    return item


@app.get("/from/task-submission/{task}/{user}")
async def from_task_submission(task: int, user: int):
    item = await prisma.tasksubmission.find_first(
        where={"user_id": user, "source_id": task})
    if not item:
        raise HTTPException(status_code=404)
    return item


@app.get("/from/task-other-submission/{task}/{user}")
async def from_task_other_submission(task: int, user: int):
    item = await prisma.tasksubmission.find_many(
        where={
            "user_id": {
                "not": user
            },
            "source_id": {
                "not": task
            }
        },
        include={
            "user": True,
        }
    )
    return item


@app.post("/task/grade")
async def grade_task(body: TaskGradeRequestBody):
    item = await prisma.taskresponse.create(
        data={
            "grade": body.grade,
            "remark": body.remark,
            "attachments": body.attachments,
            "source_id": body.source,
            "user_id": body.user,
        }
    )
    return item


@app.post("/post/submission")
async def submit_task(body: TaskSubmissionRequestBody):
    item = await prisma.tasksubmission.create(
        data={
            "desc": body.remark,
            "attachments": body.attachments,
            "source_id": body.source,
            "user_id": body.user,
        }
    )
    return item
