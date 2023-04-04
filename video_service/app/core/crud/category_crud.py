from shared.crud.base_crud import BaseCRUD
from app.database.models.category import Category
from app.api.video.schemas import CategoryCreateSchema
from shared.fastapi.exceptions import NotFoundException


class CategoryCRUD(BaseCRUD):
    Table = Category

    @classmethod
    async def get_or_create(cls, name: str) -> Category:
        try:
            instance = await cls.retrieve(name=name)
            return instance
        except NotFoundException:
            await cls.create(CategoryCreateSchema(name=name))
            instance = await cls.retrieve(name=name)
            return instance
