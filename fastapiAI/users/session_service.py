from datetime import datetime, timedelta
import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Session as UserSession
from utils.security import hash_session_token


from fastapi import Request, Depends, HTTPException

from database import get_db


class SessionService:

    def __init__(self, db: Session):
        self.db = db


    def create_session(self, user, request):

        session_token = secrets.token_urlsafe(64)

        session = UserSession(
            user_id=user.id,
            refresh_token_hash=hash_session_token(
                session_token
            ),
            expires_at=datetime.utcnow() + timedelta(days=30),
            ip_address=request.client.host
                if request.client else None,
            user_agent=request.headers.get(
                "user-agent"
            )
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session_token


    def get_user_from_session(self, session_token):

        token_hash = hash_session_token(
            session_token
        )

        session = self.db.scalar(
            select(UserSession)
            .where(
                UserSession.refresh_token_hash
                == token_hash
            )
        )

        if not session:
            return None

        if session.expires_at < datetime.utcnow():
            self.db.delete(session)
            self.db.commit()
            return None

        return session.user





def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    session_token = request.cookies.get(
        "session_id"
    )

    if not session_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    service = SessionService(db)

    user = service.get_user_from_session(
        session_token
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid session"
        )

    return user    