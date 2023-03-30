from uuid import UUID

from fastapi import File, UploadFile, Form
from pydantic import BaseModel


class CategoryCreateSchema(BaseModel):
    name: str


class VideoCreateFormRequest(BaseModel):
    title: str
    description: str
    category: str
    video: UploadFile

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        description: str = Form(...),
        category: str = Form(...),
        video: UploadFile = File(...),
    ) -> "VideoCreateFormRequest":
        return cls(title=title, description=description, category=category, video=video)


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
    items: list[VideoSerializer]
