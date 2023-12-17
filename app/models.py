from pydantic import BaseModel as Model


class BaseModel(Model):
    class Config:
        populate_by_name = True
        from_attributes = True
