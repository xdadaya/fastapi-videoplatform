from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from models import User
from token_service import TokenService


async def verify_token(request: Request, call_next):
    authorization = request.headers.get("Authorization")
    if authorization:
        try:
            user_id = TokenService.verify_token(authorization)
            user = await User.get(user_id)
            if not user:
                return JSONResponse(status_code=403, content="There is no user for that token")
            if user.is_deleted:
                return JSONResponse(status_code=403, content="There is no user for that token")
            request.state.uid = user_id
        except KeyError:
            return JSONResponse(status_code=403, content="No authorization")
    return await call_next(request)
