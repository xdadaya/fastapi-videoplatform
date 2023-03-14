from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str


class UserCreateSchema(UserSchema):
    password: str


class UserRegisterRequest(UserSchema):
    password: str
    repeat_password: str


class UserLoginRequest(UserSchema):
    password: str


class TokenSchema(BaseModel):
    access_token: str


class UserToCreate(UserSchema):
    hashed_password: str
