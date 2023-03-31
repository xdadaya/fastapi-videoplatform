from app.core.crud.base_crud import BaseCRUD
from app.database.models.comment_reaction import CommentReaction
from app.database.sessions import Propagation, Transactional
from app.database.db import session
from sqlalchemy import delete


class CommentReactionCRUD(BaseCRUD):
    Table = CommentReaction

    @classmethod
    @Transactional(propagation=Propagation.REQUIRED)
    async def delete(cls, **kwargs) -> None:
        query = cls.filter_query(query=delete(cls.Table), kwargs=kwargs)
        await session.execute(query)
