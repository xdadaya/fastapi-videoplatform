from fastapi import FastAPI

from app.api.views import api
from app.database.db import create_models
from app.core.fastapi.middleware.base_middleware import make_middleware

app = FastAPI(title="Users App", middleware=make_middleware())
app.include_router(api, prefix="/api/v1")
app.add_event_handler("startup", create_models)
