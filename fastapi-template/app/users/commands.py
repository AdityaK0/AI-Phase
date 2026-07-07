from pydantic import EmailStr

from app.core.schemas import BaseSchema

# ── CQRS: Commands are write-operation inputs ─────────────────────────────────
# Think of these like vine-protean's @vine.command classes.
# They define WHAT the client intends to do, not just what data they sent.


class CreateUserCommand(BaseSchema):
    email: EmailStr
    full_name: str
    password: str


class UpdateUserCommand(BaseSchema):
    full_name: str | None = None
    is_active: bool | None = None


class AuthenticateUserCommand(BaseSchema):
    email: EmailStr
    password: str
