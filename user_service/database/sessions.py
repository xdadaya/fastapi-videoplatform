from contextvars import Token
from enum import Enum
from functools import wraps
from typing import Callable
from uuid import uuid4

from database.db import reset_session_context, session, set_session_context


def standalone_session(func: Callable) -> Callable:
    async def _standalone_session(*args, **kwargs):
        session_id: str = str(uuid4())
        context: Token = set_session_context(session_id)

        try:
            await func(*args, **kwargs)
        except Exception as exception:
            await session.rollback()
            raise exception
        finally:
            await session.remove()
            reset_session_context(context=context)

    return _standalone_session


class Propagation(str, Enum):
    REQUIRED = "required"
    REQUIRED_NEW = "required_new"


class Transactional:
    def __init__(self, propagation: Propagation = Propagation.REQUIRED):
        self.propagation = propagation

    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            try:
                result = await function(*args, **kwargs)
                await session.commit()
            except Exception as exception:
                await session.rollback()
                raise exception
            return result
        return decorator
