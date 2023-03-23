from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException
from app.database.db_utils import connect, close_connection
from app.database.db import get_database

from app.database.models.user_statistics import UserStatisticsBaseScheme, UserStatisticsDBScheme, \
    UserStatisticsCreateScheme, UserStatisticsUpdateScheme
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


@app.get("/")
async def get_all(db=Depends(get_database)):
    return await UserStatisticsCRUD.list(db)


@app.post("/")
async def create(data: UserStatisticsCreateScheme, db=Depends(get_database)) -> None:
    await UserStatisticsCRUD.create(db, data)


@app.put("/{user_id}")
async def update(user_id: UUID, data: UserStatisticsUpdateScheme, db=Depends(get_database)) -> None:
    stats = await UserStatisticsCRUD.retrieve(db, user_id=user_id)
    await UserStatisticsCRUD.update(db, stats["_id"], **data.dict())


@app.delete("/{user_id}")
async def delete(user_id: UUID, db=Depends(get_database)) -> None:
    stats = await UserStatisticsCRUD.retrieve(db, user_id=user_id)
    await UserStatisticsCRUD.delete(db, stats["_id"])
