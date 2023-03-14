from fastapi import FastAPI

from api.views import api
from database.db import create_models
from services.base_middleware import make_middleware

app = FastAPI(title="Users App", middleware=make_middleware())
app.include_router(api, prefix="/api/v1")
app.add_event_handler("startup", create_models)
