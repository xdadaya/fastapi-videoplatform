from passlib.context import CryptContext

from app.core.crud.user_crud import UserCRUD
from app.core.fastapi.exceptions import PasswordDoNotMatchException, DuplicatedUserException, NotFoundException, \
    InvalidCredentialsException
from app.core.schemas.auth_schema import UserRegisterRequest, UserLoginRequest, UserCreateSchema, TokenSchema
from app.core.schemas.user_schema import UserSerializer
from app.services.token_service import TokenService


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
            return await UserCRUD.retrieve(username=user.username)

    @classmethod
    async def login(cls, user: UserLoginRequest) -> TokenSchema:
        try:
            user_in_db = await UserCRUD.retrieve(username=user.username)
        except NotFoundException as exc:
            raise InvalidCredentialsException() from exc
        if cls.pwd_context.verify(user.password, user_in_db.password):
            return TokenSchema(access_token=TokenService.generate_token(user_in_db.id))
        else:
            raise InvalidCredentialsException()
