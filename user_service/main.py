from fastapi import FastAPI

from database import db
from api.views import api


db.init()
app = FastAPI(title="Users App", description="Handling Our Users", version="1")


@app.on_event("startup")
async def startup():
    await db.create_all()


@app.on_event("shutdown")
async def shutdown():
    await db.close()


app.include_router(api, prefix="/api/v1")
