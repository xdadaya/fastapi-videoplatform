from passlib.context import CryptContext
from app.core.crud.user_crud import UserCRUD
from shared.fastapi.exceptions import (
    PasswordDoNotMatchException,
    DuplicatedUserException,
    NotFoundException,
    InvalidCredentialsException,
)
from app.core.schemas.auth_schema import (
    UserRegisterRequest,
    UserLoginRequest,
    UserCreateSchema,
    TokenSchema,
    RefreshTokenRequest,
)
from app.core.schemas.user_schema import UserSerializer
from app.services.token_service import TokenService
from app.producer import publish


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    async def register(cls, user: UserRegisterRequest) -> UserSerializer:
        if user.password != user.repeat_password:
            raise PasswordDoNotMatchException()
        try:
            await UserCRUD.retrieve(username=user.username)
            raise DuplicatedUserException()
        except NotFoundException:
            user.password = cls.pwd_context.hash(user.password)
            user_dict = user.dict()
            user_dict.pop("repeat_password")
            await UserCRUD.create(UserCreateSchema(**user_dict))
            user = await UserCRUD.retrieve(username=user.username)
            data = {"user_id": str(user.id)}
            await publish(send_method="create_stats", data=data)
            return user

    @classmethod
    async def login(cls, user: UserLoginRequest) -> TokenSchema:
        try:
            user_in_db = await UserCRUD.retrieve(username=user.username)
        except NotFoundException as exc:
            raise InvalidCredentialsException() from exc
        if cls.pwd_context.verify(user.password, user_in_db.password):
            access_token, refresh_token = TokenService.generate_token(user_in_db.id)
            return TokenSchema(access_token=access_token, refresh_token=refresh_token)
        else:
            raise InvalidCredentialsException()

    @classmethod
    async def refresh(cls, refresh_token: RefreshTokenRequest) -> TokenSchema:
        user_id = TokenService.verify_refresh_token(refresh_token.refresh_token)
        access_token, refresh_token = TokenService.generate_token(user_id)
        return TokenSchema(access_token=access_token, refresh_token=refresh_token)
