from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.exceptions.exc import BaseHTTPException
from services.sqlalchemy import SQLAlchemyMiddleware


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, BaseHTTPException):
        status_code = int(exc.status_code)
        error_code = exc.status_code
        message = exc.message

    return JSONResponse(
        status_code=status_code, content={"error_code": error_code, "message": message}
    )


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
