from app.core.crud.base_crud import BaseCRUD
from app.database.models.video import Video
from app.database.sessions import Propagation, Transactional
from app.database.db import session
from sqlalchemy import update


class VideoCRUD(BaseCRUD):
    Table = Video

    @classmethod
    @Transactional(propagation=Propagation.REQUIRED)
    async def delete(cls, **kwargs) -> None:
        query = cls.filter_query(
            query=update(cls.Table).values(is_deleted=True, video_url=None),
            kwargs=kwargs,
        )
        await session.execute(query)
