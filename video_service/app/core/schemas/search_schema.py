from pydantic import BaseModel


class SearchSchema(BaseModel):
    field: str
    like: str
