from datetime import datetime
from typing import Dict, Any
from uuid import uuid4

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select

# from database import Base, db
#
#
# class User(Base):
#     __tablename__ = "users"
#     id = Column(String, primary_key=True)
#     username = Column(String, unique=True)
#     hashed_password = Column(String)
#     created_at = Column(DateTime, index=True, default=datetime.utcnow)
#     is_deleted = Column(Boolean, default=False)
#
#     def __repr__(self) -> str:
#         return f"<{self.__class__.__name__} - (id={self.id}, username={self.username})>"
#
#     @classmethod
#     async def create(cls, **kwargs: Dict[Any, Any]) -> 'User':
#         user = cls(id=str(uuid4()), **kwargs)
#         db.add(user)
#         try:
#             await db.commit()
#         except Exception:
#             await db.rollback()
#             raise
#         return user
#
#     @classmethod
#     async def update(cls, user_id: str, **kwargs: Dict[Any, Any]) -> 'User':
#         query = (sqlalchemy_update(cls).where(cls.id == user_id).values(**kwargs))
#         await db.execute(query)
#         try:
#             await db.commit()
#         except Exception:
#             await db.rollback()
#             raise
#         query = select(cls).where(cls.id == user_id)
#         users = await db.execute(query)
#         users = [user[0] for user in users]
#         if len(users) > 0:
#             user = users[0]
#             return user
#
#     @classmethod
#     async def get(cls, user_id: str) -> 'User':
#         query = select(cls).where(cls.id == user_id)
#         users = await db.execute(query)
#         users = [user[0] for user in users]
#         if len(users) > 0:
#             user = users[0]
#             return user
#
#     @classmethod
#     async def get_by_username(cls, username: str) -> 'User':
#         query = select(cls).where(cls.username == username)
#         users = await db.execute(query)
#         users = [user[0] for user in users]
#         if len(users) > 0:
#             user = users[0]
#             return user
#
#     @classmethod
#     async def delete(cls, user_id: str) -> None:
#         query = sqlalchemy_update(cls).where(cls.id == user_id).values(is_deleted=True)
#         await db.execute(query)
#         try:
#             await db.commit()
#         except Exception:
#             await db.rollback()
#             raise
