from uuid import UUID

from fastapi import Request
from fastapi.responses import PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.core.crud.user_crud import UserCRUD
from app.core.fastapi.exceptions import InvalidCredentialsException
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
        user = await UserCRUD.retrieve(id=user_id)
        if not user:
            raise InvalidCredentialsException()
        if user.is_deleted:
            raise InvalidCredentialsException()
        return user_id
    except KeyError:
        raise InvalidCredentialsException()
