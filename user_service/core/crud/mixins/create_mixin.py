from pydantic import BaseModel

from core.crud.mixins.base_mixin import BaseMixin, TableType
from database.db import session
from database.sessions import Propagation, Transactional


class CreateMixin(BaseMixin):
    @classmethod
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(cls, obj: BaseModel) -> TableType:
        instance = cls.Table(**obj.dict())
        session.add(instance)
        return instance
