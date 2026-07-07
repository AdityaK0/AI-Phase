from typing import TypeVar
from app.core.schemas import PaginatedResponse

T = TypeVar("T")


def paginate(items: list[T], total: int, page: int, size: int) -> PaginatedResponse[T]:
    return PaginatedResponse(total=total, page=page, size=size, items=items)
