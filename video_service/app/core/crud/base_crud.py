from app.core.crud.mixins import (
    CreateMixin,
    DeleteMixin,
    ListMixin,
    RetrieveMixin,
    UpdateMixin,
)


class BaseCRUD(CreateMixin, RetrieveMixin, ListMixin, UpdateMixin, DeleteMixin):
    Table = None
