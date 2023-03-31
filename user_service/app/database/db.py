from contextvars import ContextVar, Token
from typing import Union

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()
Base = declarative_base()
session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engine = create_async_engine(
    settings.database_url, pool_recycle=3600, pool_pre_ping=True, echo=False
)
async_session_factory = sessionmaker(class_=AsyncSession, bind=engine)
session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory, scopefunc=get_session_context
)


async def create_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
