from sqlalchemy import select

from core.crud.base_crud import BaseCRUD
from database.db import session
from database.models.user import User


class UserCRUD(BaseCRUD):
    Table = User

    @classmethod
    async def get_by_username(cls, username: str):
        q = select(User).where(User.username == username)
        return (await session.execute(q)).scalars().first()
