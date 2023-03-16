from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import update

from app.core.crud.mixins.base_mixin import BaseMixin
from app.database.db import session
from app.database.sessions import Propagation, Transactional


class UpdateMixin(BaseMixin):
    @classmethod
    @Transactional(propagation=Propagation.REQUIRED)
    async def update(cls, id: UUID, input_data: BaseModel) -> None:
        query = (
            update(cls.Table)
            .where(cls.Table.id == id)
            .values(
                **(input_data if isinstance(input_data, dict) else input_data.__dict__)
            )
        )
        await session.execute(query)
