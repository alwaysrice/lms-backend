
from pydantic import BaseModel


class Pair(BaseModel):
    key: str
    value: object


class LoginRequestBody(BaseModel):
    username: str
    password: str


class SignupRequestBody(BaseModel):
    username: str
    password: str
    lastname: str
    firstname: str


class TaskGradeRequestBody(BaseModel):
    source: int
    user: int
    remark: str
    grade: int
    attachments: list


class TaskSubmissionRequestBody(BaseModel):
    source: int
    user: int
    remark: str
    attachments: list


class ReactRequestBody(BaseModel):
    post: int
    user: int
    reaction: str = "LIKE"


class CommentRequestBody(BaseModel):
    post: int
    user: int
    text: str


class CreatePostRequestBody(BaseModel):
    source: int
    group: int
    desc: str
    title: str
    cover: str
    attachments: list[str]
