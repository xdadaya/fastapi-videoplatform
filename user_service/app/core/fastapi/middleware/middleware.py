from uuid import UUID

from fastapi import Request

from app.core.crud.user_crud import UserCRUD
from app.core.fastapi.exceptions import InvalidCredentialsException
from app.services.token_service import TokenService


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
