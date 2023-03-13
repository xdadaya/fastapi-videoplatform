from fastapi import APIRouter, Depends
from passlib.context import CryptContext

from core.exceptions.exc import PasswordDoNotMatchException, DuplicatedUserException, NotFoundException, \
    InvalidCredentialsException
from core.schemas.auth_schema import UserRegisterRequest, UserLoginRequest, UserToCreate, UserSchema, TokenSchema
from core.schemas.user_schema import UserSerializer
from models import User
from services.middleware import verify_token
from services.token_service import TokenService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
api = APIRouter(prefix="/users", )


@api.post("/register", response_model=UserSerializer, status_code=201)
async def register_user(user: UserRegisterRequest) -> UserSerializer:
    if user.password != user.repeat_password:
        raise PasswordDoNotMatchException()
    user_in_db = await User.get_by_username(user.username)
    if user_in_db:
        raise DuplicatedUserException()
    user = UserToCreate(username=user.username, hashed_password=pwd_context.hash(user.password))
    user = await User.create(**user.dict())
    return user


@api.post("/login", response_model=TokenSchema)
async def login_user(user: UserLoginRequest) -> TokenSchema:
    user_in_db = await User.get_by_username(user.username)
    if user_in_db:
        if user_in_db.is_deleted:
            raise InvalidCredentialsException()
        if pwd_context.verify(user.password, user_in_db.hashed_password):
            return TokenSchema(access_token=TokenService.generate_token(user_in_db.id))
        else:
            raise InvalidCredentialsException()
    raise InvalidCredentialsException()


@api.get("/me", response_model=UserSerializer)
async def get_user_data(user_id: str = Depends(verify_token)) -> UserSerializer:
    user = await User.get(user_id)
    if user is None:
        raise NotFoundException()
    return user


@api.put("/me", response_model=UserSerializer)
async def update_user_data(user: UserSchema, user_id: str = Depends(verify_token)) -> UserSerializer:
    user_in_db = await User.get_by_username(user.username)
    if user_in_db:
        raise DuplicatedUserException()
    user = await User.update(user_id, **user.dict())
    return user


@api.delete("/me", status_code=200)
async def delete_user(user_id: str = Depends(verify_token)) -> None:
    await User.delete(user_id)
