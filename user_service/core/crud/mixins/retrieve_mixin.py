from sqlalchemy import select

from core.crud.mixins.base_mixin import BaseMixin, TableType
from database.db import session


class RetrieveMixin(BaseMixin):
    @classmethod
    async def retrieve(cls, **kwargs) -> TableType:
        result = await session.execute(
            cls.filter_query(query=select(cls.Table), kwargs=kwargs)
        )
        obj = result.scalars().first()
        cls._check_object(obj)
        await session.refresh(obj)
        return obj
