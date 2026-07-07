from app.core.schemas import TimestampSchema

# ── CQRS: Schemas are read-operation outputs (responses only) ─────────────────
# Commands live in commands.py. This file only has what the API returns.


class UserResponse(TimestampSchema):
    id: int
    email: str
    full_name: str
    is_active: bool
    # hashed_password intentionally excluded
