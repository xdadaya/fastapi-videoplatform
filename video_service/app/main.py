from fastapi import FastAPI, HTTPException

from app.database.db import create_models, check_db
from shared.fastapi.middleware.base_middleware import make_middleware
from shared.fastapi.middleware.middleware import MaintainceModeMiddleware
from app.api.api import api


app = FastAPI(title="Videos App", middleware=make_middleware())
app.add_middleware(MaintainceModeMiddleware)
app.add_event_handler("startup", create_models)
app.include_router(api)


@app.get("/healthcheck")
async def healthcheck() -> dict[str, bool]:
    result = await check_db()
    if not result:
        raise HTTPException(503)
    return {"ok": result}
