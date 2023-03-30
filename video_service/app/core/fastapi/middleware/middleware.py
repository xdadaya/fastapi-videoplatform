from uuid import UUID

from fastapi import Request
from fastapi.responses import PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.core.fastapi.exceptions import InvalidCredentialsException, NotOwnerException
from app.services.token_service import TokenService
from app.core.crud.video_crud import VideoCRUD
from app.core.crud.comment_crud import CommentCRUD
from app.core.config import get_settings


settings = get_settings()


class MaintainceModeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if settings.MAINTAINCE_MODE:
            return PlainTextResponse(content='Maintaince mode is on. Server is unavailable')
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


async def is_video_owner(request: Request) -> None:
    authorization = request.headers.get("Authorization")
    if authorization is None:
        raise InvalidCredentialsException()
    try:
        user_id = TokenService.verify_token(authorization)
    except KeyError:
        raise InvalidCredentialsException()
    video_id = request.path_params['video_id']
    video = await VideoCRUD.retrieve(id=video_id)
    if video.owner_id != user_id:
        raise NotOwnerException()


async def is_comment_owner(request: Request) -> None:
    authorization = request.headers.get("Authorization")
    if authorization is None:
        raise InvalidCredentialsException()
    try:
        user_id = TokenService.verify_token(authorization)
    except KeyError:
        raise InvalidCredentialsException()
    comment_id = request.path_params['comment_id']
    comment = await CommentCRUD.retrieve(id=comment_id)
    if comment.owner_id != user_id:
        raise NotOwnerException()
