from fastapi import Request

from core.exceptions.exc import InvalidCredentialsException
from models import User
from services.token_service import TokenService


async def verify_token(request: Request) -> str:
    authorization = request.headers.get("Authorization")
    if authorization is None:
        raise InvalidCredentialsException()
    try:
        user_id = TokenService.verify_token(authorization)
        user = await User.get(user_id)
        if not user:
            raise InvalidCredentialsException()
        if user.is_deleted:
            raise InvalidCredentialsException()
        return user_id
    except KeyError:
        raise InvalidCredentialsException()
