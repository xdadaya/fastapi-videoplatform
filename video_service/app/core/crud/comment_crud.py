from app.core.crud.base_crud import BaseCRUD
from app.database.models.comment import Comment


class CommentCRUD(BaseCRUD):
    Table = Comment
