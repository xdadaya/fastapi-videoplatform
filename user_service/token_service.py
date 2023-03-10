from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from config import get_settings

settings = get_settings()


class TokenService:
    @staticmethod
    def generate_token(user_id: str) -> str:
        expires_at = datetime.now() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({
            'id': user_id,
            'exp': expires_at
        }, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM)
        return token

    @staticmethod
    def verify_token(authorization: str) -> str:
        token_header, token = authorization.split(" ")
        if token_header.lower() != settings.AUTHENTICATION_HEADER_PREFIX.lower():
            raise HTTPException(status_code=403, detail='Authentication error. Unable to decode token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.HASH_ALGORITHM)
        except Exception:
            raise HTTPException(status_code=403, detail='Authentication error. Unable to decode token')

        if payload["exp"] < int(datetime.now().timestamp()):
            raise HTTPException(status_code=403, detail='Token is expired')

        return payload["id"]
