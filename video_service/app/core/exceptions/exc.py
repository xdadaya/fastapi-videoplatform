from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN


class BaseHTTPException(HTTPException):
    status_code: int = HTTP_400_BAD_REQUEST
    detail: str = "Error"

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class UnauthorizedException(BaseHTTPException):
    status_code = HTTP_401_UNAUTHORIZED
    detail = "Unauthorized"


class NotFoundException(BaseHTTPException):
    status_code = HTTP_404_NOT_FOUND
    detail = "Not found"


class InvalidCredentialsException(BaseHTTPException):
    detail = "Invalid credentials"


class NotOwnerException(BaseHTTPException):
    status_code = HTTP_403_FORBIDDEN
    detail = "Forbidden"
