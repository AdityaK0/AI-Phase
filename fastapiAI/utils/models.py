
from database import Base
from sqlalchemy import DateTime,Boolean
from sqlalchemy.orm import mapped_column,Mapped
from datetime import datetime

class BaseModel(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    