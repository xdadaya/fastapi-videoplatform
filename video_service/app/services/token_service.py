from uuid import UUID

import jwt
from fastapi import HTTPException

from app.core.config import get_settings

settings = get_settings()


class TokenService:
    @staticmethod
    def verify_token(authorization: str) -> UUID:
        token_header, token = authorization.split(" ")
        if token_header.lower() != settings.AUTHENTICATION_HEADER_PREFIX.lower():
            raise HTTPException(status_code=403, detail='Authentication error. Unable to decode token')
        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.HASH_ALGORITHM)
        except Exception:
            raise HTTPException(status_code=403, detail='Authentication error. Unable to decode token')
        return UUID(payload["id"])
