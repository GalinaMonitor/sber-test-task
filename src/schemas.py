from datetime import datetime
from typing import Any, List

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class DatetimeQueryParams(PydanticBaseModel):
    from_timestamp: datetime = None
    to_timestamp: datetime = None


class ResponseStatus(PydanticBaseModel):
    status: Any


class ResponseDomains(PydanticBaseModel):
    status: Any
    domains: List[str]


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)


class LinkView(BaseModel):
    link: str
    domain_id: int
    viewed_at: datetime


class Domain(BaseModel):
    id: int
    name: str
