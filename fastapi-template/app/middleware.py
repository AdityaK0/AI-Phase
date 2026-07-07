from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.database import SessionLocal, _request_session


class DBSessionMiddleware(BaseHTTPMiddleware):
    """
    Opens a DB session at the start of every request, stores it in a ContextVar,
    commits on success, rolls back on any exception, always closes.

    This means NO route, service, or repository ever receives a `db` parameter —
    they call database.get_session() internally instead.
    """

    async def dispatch(self, request: Request, call_next):
        session = SessionLocal()
        token = _request_session.set(session)
        try:
            response = await call_next(request)
            session.commit()
            return response
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            _request_session.reset(token)  # clean up for the next request
