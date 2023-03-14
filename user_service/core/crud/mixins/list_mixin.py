from typing import Optional

from sqlalchemy import select, and_

from core.crud.mixins.base_mixin import BaseMixin, TableType
from core.schemas.search_schema import SearchSchema
from database.db import session


class ListMixin(BaseMixin):
    @classmethod
    async def list_items(cls, **kwargs) -> list[TableType]:
        query = cls.filter_query(query=select(cls.Table), kwargs=kwargs)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def search_list_query(cls, search_schema: Optional[list[SearchSchema]] = None, **kwargs) -> list[TableType]:
        query = cls.filter_query(query=select(cls.Table), kwargs=kwargs)
        all_columns = cls.Table.__dict__
        search_item: SearchSchema
        conditions = [
            getattr(cls.Table, search_item.field).ilike(f"%{search_item.like}%")
            for search_item in search_schema
        ]
        query = query.where(and_(*conditions))
        return (await session.execute(query)).scalars().all()