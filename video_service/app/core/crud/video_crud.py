from app.core.crud.base_crud import BaseCRUD
from app.database.models.video import Video


class VideoCRUD(BaseCRUD):
    Table = Video
