from datetime import datetime, timedelta
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

    @staticmethod
    def generate_token(user_id: UUID) -> str:
        expires_at = datetime.now() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({
            'id': str(user_id),
            'exp': expires_at
        }, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM)
        return token
