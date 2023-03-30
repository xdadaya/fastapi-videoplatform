from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException
from app.database.db_utils import connect, close_connection
from app.database.db import get_database

from app.database.models.user_statistics import (
    UserStatisticsResponseScheme,
    UserStatisticsBaseScheme,
)
from app.core.crud.user_statistics_crud import UserStatisticsCRUD
from app.core.middleware.middleware import MaintainceModeMiddleware


app = FastAPI(title="Statistics App")
app.add_middleware(MaintainceModeMiddleware)
app.add_event_handler("startup", connect)
app.add_event_handler("shutdown", close_connection)


@app.get("/{user_id}", response_model=UserStatisticsResponseScheme)
async def index(
    user_id: UUID, db=Depends(get_database)
) -> UserStatisticsResponseScheme:
    result = UserStatisticsBaseScheme(
        **(await UserStatisticsCRUD.retrieve(db, user_id=user_id))
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    avg_rating = (
        result.total_rating / result.comments_amount
        if result.comments_amount != 0
        else 0
    )
    avg_text_length = (
        result.total_text_length / result.comments_amount
        if result.comments_amount != 0
        else 0
    )
    avg_comments_per_video = (
        result.comments_amount / result.videos_amount
        if result.videos_amount != 0
        else 0
    )
    return UserStatisticsResponseScheme(
        user_id=result.user_id,
        comments_amount=result.comments_amount,
        avg_rating=avg_rating,
        avg_text_length=avg_text_length,
        avg_comments_per_video=avg_comments_per_video,
    )
