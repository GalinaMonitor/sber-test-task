from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class DatetimeQueryParams(PydanticBaseModel):
    from_timestamp: datetime = None
    to_timestamp: datetime = None


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)


class LinkView(BaseModel):
    link: str
    domain_id: int
    viewed_at: datetime


class Domain(BaseModel):
    id: int
    name: str
