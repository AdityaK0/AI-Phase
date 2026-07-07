from contextvars import ContextVar

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.APP_DEBUG,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


# ── request-scoped session ────────────────────────────────────────────────────
# DBSessionMiddleware sets this once per request.
# Every repository reads it via get_session() — no db passed anywhere.
# Same idea as Protean's domain_context() in vine-protean / vfc.
_request_session: ContextVar[Session | None] = ContextVar(
    "request_session", default=None
)


def get_session() -> Session:
    session = _request_session.get()
    if session is None:
        raise RuntimeError(
            "No DB session for this request. "
            "Is DBSessionMiddleware added in main.py?"
        )
    return session


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
