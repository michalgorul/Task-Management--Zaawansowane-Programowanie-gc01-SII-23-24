from pydantic import BaseModel as Model, ConfigDict


class BaseModel(Model):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
