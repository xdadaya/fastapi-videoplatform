from uuid import UUID

from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from core.schemas.auth_schema import UserRegisterRequest, UserLoginRequest, TokenSchema, UserSchema
from core.schemas.user_schema import UserSerializer
from services.middleware import verify_token
from api.auth_service import AuthService
from api.user_service import UserService


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
api = APIRouter(prefix="/users", )


@api.post("/register", response_model=UserSerializer, status_code=201)
async def register_user(user: UserRegisterRequest) -> UserSerializer:
    return await AuthService.register(user)


@api.post("/login", response_model=TokenSchema)
async def login_user(user: UserLoginRequest) -> TokenSchema:
    return await AuthService.login(user)


@api.get("/me", response_model=UserSerializer)
async def get_user_data(user_id: UUID = Depends(verify_token)) -> UserSerializer:
    return await UserService.get_user(user_id)


@api.put("/me", response_model=UserSerializer)
async def update_user_data(user: UserSchema, user_id: UUID = Depends(verify_token)) -> UserSerializer:
    return await UserService.update_user(user, user_id)


@api.delete("/me", status_code=200)
async def delete_user(user_id: UUID = Depends(verify_token)) -> None:
    await UserService.delete_user(user_id)
