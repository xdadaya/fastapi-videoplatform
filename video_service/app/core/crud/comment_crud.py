from app.core.crud.base_crud import BaseCRUD
from app.database.models.comment import Comment
from app.database.sessions import Propagation, Transactional
from app.database.db import session
from sqlalchemy import text, func, desc
from sqlalchemy.sql import select
from math import ceil
from app.api.comment.schemas import CommentListResponse


class CommentCRUD(BaseCRUD):
    Table = Comment

    @classmethod
    @Transactional(propagation=Propagation.REQUIRED)
    async def custom_list_items(cls, page, limit, sort, **kwargs) -> CommentListResponse:
        query = cls.filter_query(query=select(cls.Table), kwargs=kwargs)
        if sort:
            sort = sort.replace("rating", "anon_3")
            if sort[0] == "-":
                sort = sort[1:]
                query = query.order_by(desc(sort))
            else:
                query = query.order_by(sort)

        count_query = select(func.count(1)).select_from(query)

        offset_page = page - 1
        query = (query.offset(offset_page * limit).limit(limit))

        total_record = (await session.execute(count_query)).scalar() or 0

        total_page = ceil(total_record / limit)

        result = await session.execute(query)
        result = result.scalars().all()

        return CommentListResponse(
            page_number=page, page_size=limit, total_pages=total_page, content=result
        )
