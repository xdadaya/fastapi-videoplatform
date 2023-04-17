from typing import Union
from uuid import UUID

from httpx import AsyncClient
from pydantic import BaseModel

from shared.fastapi.exceptions import BaseHTTPException


class OwnerSerializer(BaseModel):
    id: Union[UUID, None]
    username: str


async def get_user_data(user_id: UUID) -> OwnerSerializer:
    async with AsyncClient() as client:
        response = await client.get(
            f"http://user_service:5000/api/v1/users/user/{user_id}"
        )
        if response.status_code == 200:
            data = response.json()
            return OwnerSerializer(**data)
        elif response.status_code == 404:
            return OwnerSerializer(owner_id=None, username="[DELETED]")
        else:
            raise BaseHTTPException()
