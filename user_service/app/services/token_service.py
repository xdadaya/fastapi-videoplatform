from datetime import datetime, timedelta
from uuid import UUID

import jwt
from fastapi import HTTPException

from app.core.config import get_settings

settings = get_settings()


class TokenService:
    @staticmethod
    def generate_token(user_id: UUID) -> str:
        expires_at = datetime.now() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        access_token = jwt.encode(
            {"id": str(user_id), "type": "access", "exp": expires_at},
            settings.SECRET_KEY,
            algorithm=settings.HASH_ALGORITHM,
        )
        expires_at = datetime.now() + timedelta(days=30)
        refresh_token = jwt.encode(
            {"id": str(user_id), "type": "refresh", "exp": expires_at},
            settings.SECRET_KEY,
            algorithm=settings.HASH_ALGORITHM,
        )
        return access_token, refresh_token

    @staticmethod
    def verify_token(authorization: str) -> UUID:
        token_header, token = authorization.split(" ")
        if token_header.lower() != settings.AUTHENTICATION_HEADER_PREFIX.lower():
            raise HTTPException(
                status_code=403, detail="Authentication error. Unable to decode token"
            )
        try:
            payload = jwt.decode(
                token, key=settings.SECRET_KEY, algorithms=settings.HASH_ALGORITHM
            )
        except Exception:
            raise HTTPException(
                status_code=403, detail="Authentication error. Unable to decode token"
            )
        if payload["type"] == "access":
            return UUID(payload["id"])
        raise HTTPException(
            status_code=403, detail="Authentication error. Its not valid access token"
        )

    @staticmethod
    def verify_refresh_token(refresh_token: str) -> UUID:
        try:
            payload = jwt.decode(
                refresh_token,
                key=settings.SECRET_KEY,
                algorithms=settings.HASH_ALGORITHM,
            )
        except Exception:
            raise HTTPException(
                status_code=403, detail="Authentication error. Unable to decode token"
            )
        if payload["type"] == "refresh":
            return UUID(payload["id"])
        raise HTTPException(
            status_code=403, detail="Authentication error. Its not valid refresh token"
        )
