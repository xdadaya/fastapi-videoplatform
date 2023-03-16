from uuid import UUID

from app.core.crud.user_crud import UserCRUD
from app.core.exceptions.exc import DuplicatedUserException, NotFoundException
from app.core.schemas.auth_schema import UserSchema
from app.core.schemas.user_schema import UserSerializer


class UserService:
    @staticmethod
    async def get_user(user_id: UUID) -> UserSerializer:
        return await UserCRUD.retrieve(id=user_id)

    @staticmethod
    async def update_user(user: UserSchema, user_id: UUID) -> UserSerializer:
        try:
            await UserCRUD.retrieve(username=user.username)
            raise DuplicatedUserException
        except NotFoundException:
            await UserCRUD.update(id=user_id, input_data=user)
        return await UserCRUD.retrieve(id=user_id)

    @staticmethod
    async def delete_user(user_id: UUID) -> None:
        await UserCRUD.delete(id=user_id)
