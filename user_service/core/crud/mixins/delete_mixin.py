from sqlalchemy import update

from core.crud.mixins.base_mixin import BaseMixin, TableType
from database.db import session
from database.sessions import Propagation, Transactional


class DeleteMixin(BaseMixin):
    @classmethod
    @Transactional(propagation=Propagation.REQUIRED)
    async def delete(cls, **kwargs) -> None:
        query = cls.filter_query(query=update(cls.Table).values(is_deleted=True), kwargs=kwargs)
        await session.execute(query)
