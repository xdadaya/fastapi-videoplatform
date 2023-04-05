from pydantic import BaseModel

from shared.crud.mixins.base_mixin import BaseMixin, TableType
from app.database.db import session
from app.database.sessions import Propagation, Transactional


class CreateMixin(BaseMixin):
    @classmethod
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(cls, obj: BaseModel) -> TableType:
        instance = cls.Table(**obj.dict())
        session.add(instance)
        return instance
