from utils.models import BaseModel
from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy import String, Integer,ForeignKey,DateTime
from datetime import datetime

class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    
    fullname: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(15),
        unique=True,
        nullable=True
    )
    
    sessions: Mapped[list["Session"]] = relationship(
        back_populates="user",
        cascade="all, delete"
    )



class Session(BaseModel):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    refresh_token_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(50)
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(255)
    )

    last_used_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    
    user: Mapped["User"] = relationship(
        back_populates="sessions"
    )
