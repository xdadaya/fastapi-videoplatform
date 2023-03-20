from fastapi import FastAPI

from app.database.db import create_models
from app.services.base_middleware import make_middleware
from app.api.api import api


app = FastAPI(title="Videos App", middleware=make_middleware())
app.add_event_handler("startup", create_models)
app.include_router(api)
