from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseSchema(BaseModel):
    # from_attributes=True lets pydantic read SQLAlchemy ORM objects directly
    # replaces the old orm_mode = True from pydantic v1
    model_config = ConfigDict(from_attributes=True)


class TimestampSchema(BaseSchema):
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseSchema):
    message: str


class PaginatedResponse(BaseSchema, Generic[T]):
    total: int
    page: int
    size: int
    items: list[T]
