from sqlalchemy import select

from core.crud.base_crud import BaseCRUD
from database.db import session
from database.models.user import User


class UserCRUD(BaseCRUD):
    Table = User
