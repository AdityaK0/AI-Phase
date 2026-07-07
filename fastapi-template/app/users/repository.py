from sqlalchemy import select

from app.core.repository import BaseRepository
from app.users.model import User


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    # ── queries ──────────────────────────────────────────────────────────────

    def get_by_email(self, email: str) -> User | None:
        return self.db.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

    def get_active_users(self, skip: int = 0, limit: int = 100):
        return self.db.execute(
            select(User).where(User.is_active == True).offset(skip).limit(limit)
        ).scalars().all()

    # ── factory — service passes data, repository builds the model ───────────
    # This keeps service.py free of any ORM imports.
    # Swap DB? Rewrite this method only — service.create() stays identical.

    def build(self, email: str, full_name: str, hashed_password: str) -> User:
        return User(email=email, full_name=full_name, hashed_password=hashed_password)
