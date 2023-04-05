from shared.crud.base_crud import BaseCRUD
from app.database.models.user import User


class UserCRUD(BaseCRUD):
    Table = User
