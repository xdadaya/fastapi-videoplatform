from typing import Union
from uuid import UUID

from fastapi import Request
from fastapi.responses import PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from shared.fastapi.exceptions import InvalidCredentialsException
from app.services.token_service import TokenService
from app.core.config import get_settings


settings = get_settings()


class MaintainceModeMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        if settings.MAINTAINCE_MODE:
            return PlainTextResponse(
                content="Maintaince mode is on. Server is unavailable"
            )
        return response


async def verify_token(request: Request) -> UUID:
    authorization = request.headers.get("Authorization")
    if authorization is None:
        raise InvalidCredentialsException()
    try:
        user_id = TokenService.verify_token(authorization)
        return user_id
    except KeyError:
        raise InvalidCredentialsException()


async def get_user_id(request: Request) -> Union[UUID, None]:
    authorization = request.headers.get("Authorization")
    if authorization is None:
        return None
    try:
        user_id = TokenService.verify_token(authorization)
        return user_id
    except KeyError:
        return None
