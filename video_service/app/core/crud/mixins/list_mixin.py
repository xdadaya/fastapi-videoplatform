from typing import Optional

from sqlalchemy import select, and_, func, desc, text

from app.core.crud.mixins.base_mixin import BaseMixin, TableType
from app.core.schemas.search_schema import SearchSchema
from app.database.db import session


class ListMixin(BaseMixin):
    @classmethod
    async def list_items(cls, **kwargs) -> list[TableType]:
        query = cls.filter_query(query=select(cls.Table), kwargs=kwargs)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    def sort_items(cls, sort: str, **kwargs) -> select:
        query = cls.filter_query(query=select(cls.Table), kwargs=kwargs)
        if sort:
            if sort[0] == "-":
                sort = sort[1:]
                query = query.order_by(desc(text(sort)))
            else:
                query = query.order_by(text(sort))
        return query

    @classmethod
    async def list_items_with_pagination(cls, page: int, limit: int, sort: str = None, **kwargs) -> list[TableType]:
        query = cls.sort_items(sort, **kwargs)
        offset_page = page - 1
        query = (query.offset(offset_page * limit).limit(limit))
        result = await session.execute(query)
        result = result.scalars().all()
        return result

    @classmethod
    async def count_query(cls, **kwargs) -> int:
        query = cls.filter_query(select(cls.Table), kwargs=kwargs)
        query = (select(func.count(1))).select_from(query)
        result = await session.execute(query)
        result = result.scalars().first()
        return result

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