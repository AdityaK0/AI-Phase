
from sqlalchemy.orm import Session
from .models import User
from exceptions import AppException
from sqlalchemy import select
from utils.security import hash_password,verify_password
    
from .session_service import SessionService

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def authenticate(self,username,password):
        user = self.db.scalar(
            select(User).where(User.username == username)
        )
        
        if user and verify_password(password,user.hashed_password):
            return user
        
        return False

    def register(self, data):
         
        username = self.db.scalar(select(User).where(
            User.username == data.username
        ))
        if username:
            raise AppException("Username already exists")
        
        email = self.db.scalar (select(User).where(
            User.email == data.email
        ))
        if email:
            raise AppException("Email already exists")
        
        if data.phone_number:
            phone_number = self.db.scalar (select(User).where(
                User.phone_number == data.phone_number
                
            ))
            if phone_number:
               raise AppException("Phone already registered")
        
        
        user = User(
            fullname = data.fullname,
            email = data.email,
            username = data.username,
            phone_number = data.phone_number,
            hashed_password = hash_password(data.password)
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
        
    def login(self, command,request=None):
        user = self.authenticate(command.username, command.password)

        if not user:
            raise AppException("Invalid username or password")
        
        session_service = SessionService(self.db)

        return session_service.create_session(
            user=user,
            request=request
        )