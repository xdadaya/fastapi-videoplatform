from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException
from app.database.db_utils import connect, close_connection
from app.database.db import get_database

from app.database.models.user_statistics import UserStatisticsDBScheme, UserStatisticsCreateScheme, \
    UserStatisticsUpdateScheme
from app.core.crud.user_statistics_crud import UserStatisticsCRUD


app = FastAPI(title="Statistics App")
app.add_event_handler('startup', connect)
app.add_event_handler('shutdown', close_connection)


@app.get("/{user_id}")
async def index(user_id: UUID, db=Depends(get_database)) -> UserStatisticsDBScheme:
    result = await UserStatisticsCRUD.retrieve(db, user_id=user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    return result
