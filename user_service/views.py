from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from passlib.context import CryptContext
from pydantic import BaseModel

from models import User
from token_service import TokenService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserSchema(BaseModel):
    username: str


class UserAuth(UserSchema):
    password: str


class UserToCreate(UserSchema):
    hashed_password: str


class UserSerializer(BaseModel):
    id: str
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


api = APIRouter(prefix="/users", )


@api.post("/register", response_model=UserSerializer)
async def register_user(user: UserAuth) -> UserSerializer:
    user_in_db = await User.get_by_username(user.username)
    if user_in_db:
        raise HTTPException(status_code=400, detail="This username is taken")
    user = UserToCreate(username=user.username, hashed_password=pwd_context.hash(user.password))
    user = await User.create(**user.dict())
    return user


@api.post("/login", response_model=str)
async def login_user(user: UserAuth) -> str:
    user_in_db = await User.get_by_username(user.username)
    user_in_db = user_in_db
    if pwd_context.verify(user.password, user_in_db.hashed_password):
        return TokenService.generate_token(user_in_db.id)
    return "Wrong password"


@api.get("/me", response_model=UserSerializer)
async def get_user_data(request: Request) -> UserSerializer:
    user = await User.get(request.state.uid)
    if user is None:
        raise HTTPException(status_code=404, detail="No user with that id")
    return user


@api.put("/me", response_model=UserSerializer)
async def update_user_data(request: Request, user: UserSchema) -> UserSerializer:
    user = await User.update(request.state.uid, **user.dict())
    return user


@api.delete("/me")
async def delete_user(request: Request) -> None:
    await User.delete(request.state.uid)
