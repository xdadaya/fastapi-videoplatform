from uuid import UUID

from fastapi import Request

from app.core.exceptions.exc import InvalidCredentialsException, NotOwnerException
from app.services.token_service import TokenService
from app.core.crud.video_crud import VideoCRUD


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

