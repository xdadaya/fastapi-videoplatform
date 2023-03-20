from fastapi import APIRouter
from app.api.video.api import api as video_api

api = APIRouter(prefix="/api/v1")
api.include_router(video_api, tags=["Videos"])

