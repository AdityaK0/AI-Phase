from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, get_session

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic CRUD base. Session is NOT passed in — it's read from the
    request-scoped ContextVar via get_session().

    Every module's repository extends this with module-specific queries.
    """

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    @property
    def db(self) -> Session:
        return get_session()

    def get_by_id(self, id: int) -> ModelType | None:
        return self.db.get(self.model, id)

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        return self.db.execute(
            select(self.model).offset(skip).limit(limit)
        ).scalars().all()

    def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.flush()       # write within the open transaction
        self.db.refresh(obj)  # reload to get DB-generated id + timestamps
        return obj

    def delete(self, obj: ModelType) -> None:
        self.db.delete(obj)
        self.db.flush()
