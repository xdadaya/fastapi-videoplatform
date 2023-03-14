from typing import Generic, TypeVar, Union

from sqlalchemy import and_
from sqlalchemy.sql import expression

from core.exceptions.exc import NotFoundException

TableType = TypeVar("TableType")


class BaseMixin:
    Table: Generic[TableType]

    @classmethod
    def filter_query(cls, query: expression, kwargs: dict) -> expression:
        filter_list = [
            getattr(cls.Table, key) == value for key, value in kwargs.items()
        ]
        return query.where(and_(True, *filter_list))

    @classmethod
    def _check_object(cls, obj: TableType) -> Union[bool, NotFoundException]:
        if not obj:
            raise NotFoundException()
        return True
