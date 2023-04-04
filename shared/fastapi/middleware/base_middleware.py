from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from shared.fastapi.middleware.sqlalchemy import SQLAlchemyMiddleware


def make_middleware() -> list[Middleware]:
    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(SQLAlchemyMiddleware),
    ]
    return middlewares
