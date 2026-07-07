from fastapi import APIRouter, status

from app.core.schemas import MessageResponse
from app.users.commands import CreateUserCommand, UpdateUserCommand
from app.users.schemas import UserResponse
from app.users.service import UserService

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(command: CreateUserCommand):
    return UserService().create(command)


@router.get("/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10):
    return UserService().list(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return UserService().get(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, command: UpdateUserCommand):
    return UserService().update(user_id, command)


@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(user_id: int):
    UserService().delete(user_id)
    return {"message": "User deleted"}
