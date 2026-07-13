from fastapi import APIRouter,Depends,Request,Response
from sqlalchemy.orm import Session
from database import get_db
from .schema import CreateUser,LoginSchema
from .service import UserService
from .session_service import get_current_user
user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/register")
def regsiter(data: CreateUser,db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.register(data)
    return {"message": "User created successfully", "user": user}

@user_router.post("/login")
def login(
    command: LoginSchema,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):

    service = UserService(db)

    session_token = service.login(
        command,
        request
    )

    response.set_cookie(
        key="session_id",
        value=session_token,
        httponly=True,
        secure=False,  # True in production HTTPS
        max_age=60 * 60 * 24 * 30
    )

    return {
        "message": "Login successful"
    }
    
  
@user_router.get("/profile")
def profile(
    user = Depends(get_current_user)
):
    return {
        "username": user.username,
        "email": user.email
    }