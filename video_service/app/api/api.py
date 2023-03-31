from fastapi import APIRouter
from app.api.video.api import api as video_api
from app.api.comment.api import api as comment_api

api = APIRouter(prefix="/api/v1")
api.include_router(video_api, tags=["Videos"])
api.include_router(comment_api, tags=["Comments"])
