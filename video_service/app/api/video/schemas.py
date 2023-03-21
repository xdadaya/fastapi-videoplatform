from typing import List
from uuid import UUID

from fastapi import File
from pydantic import BaseModel


class CategoryCreateSchema(BaseModel):
    name: str


class VideoCreateRequest(BaseModel):
    title: str
    description: str
    category: str
    video: bytes = File()


class VideoCreateSchema(BaseModel):
    id: UUID
    title: str
    description: str
    video_url: str
    owner_id: UUID
    category_id: UUID


class VideoUpdateRequest(BaseModel):
    title: str
    description: str
    category: str


class VideoUpdateSchema(BaseModel):
    title: str
    description: str
    category_id: UUID


class VideoSerializer(BaseModel):
    id: UUID
    owner_id: UUID
    category_id: UUID
    title: str
    description: str
    video_url: str

    class Config:
        orm_mode = True


class VideoListResponse(BaseModel):
    page_number: int
    page_size: int
    total_pages: int
    items: List[VideoSerializer]
