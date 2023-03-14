from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND


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


class DuplicatedUserException(BaseHTTPException):
    detail = "This username is taken."


class PasswordDoNotMatchException(BaseHTTPException):
    detail = "Passwords don't match"


class InvalidCredentialsException(BaseHTTPException):
    status_code = HTTP_401_UNAUTHORIZED
    detail = "Invalid credentials"
