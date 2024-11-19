import jwt
import time
import bcrypt
from decouple import config
from typing import Annotated
from fastapi import HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from lib.db import prisma
from models.request import SignupRequestBody
from typing import Any


JWT_ALGORITHM = config("JWT_ALGORITHM")
JWT_SECRET = config("JWT_SECRET")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app = APIRouter(
    tags=["auth"]
)


def sign_jwt(username: str) -> dict[str, str]:
    payload = {
        "username": username,
        "expires": time.time() + (60 * 60 * 60 * 24)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(
        token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    # print("Time", time.time(), "<", decoded_token["expires"])
    return decoded_token if decoded_token["expires"] >= time.time() else None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        username: str = payload["username"]
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await prisma.user.find_unique(
        where={"username": username},
        include={
            "member_groups": True,
            "admin_groups": True,
            "tasks": True,
            "notifications": True,
        })
    if user is None:
        raise credentials_exception
    return user


@app.post("/login")
async def login(body: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await prisma.user.find_unique(
        where={
            "username": body.username,
        }
    )
    if not (user and bcrypt.checkpw(str.encode(body.password), str.encode(user.password))):
        raise HTTPException(status_code=401)

    token = sign_jwt(body.username)
    return {
        "access_token": token,
        "token_type": "bearer",
    }


@app.post("/signup")
async def signup(body: SignupRequestBody):
    await prisma.user.create(
        data={
            "username": body.username,
            "password": body.password,
            "firstname": body.firstname,
            "lastname": body.lastname,
        }
    )
    return sign_jwt(body.username)


@app.get("/auth")
async def auth(user: Annotated[Any, Depends(get_current_user)]):
    # print(user.member_groups)
    return user
